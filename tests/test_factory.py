"""Tests for the message and topic factories."""

import json
import logging

import pytest

from qbusmqttapi.const import TOPIC_PREFIX
from qbusmqttapi.discovery import QbusMqttDevice
from qbusmqttapi.factory import QbusMqttMessageFactory, QbusMqttTopicFactory
from qbusmqttapi.state import (
    QbusMqttAnalogState,
    QbusMqttOnOffState,
    QbusMqttState,
    StateType,
)

DISCOVERY_PAYLOAD = json.dumps(
    {
        "app": "abc",
        "devices": [
            {
                "id": "UL1",
                "serialNr": "000001",
                "functionBlocks": [{"id": "UL15", "type": "onoff"}],
            }
        ],
    }
)


@pytest.fixture
def factory() -> QbusMqttMessageFactory:
    """Return a message factory."""
    return QbusMqttMessageFactory()


@pytest.fixture
def device() -> QbusMqttDevice:
    """Return a device."""
    return QbusMqttDevice({"id": "UL1"})


@pytest.mark.parametrize(
    "payload",
    [
        DISCOVERY_PAYLOAD,
        DISCOVERY_PAYLOAD.encode(),
        bytearray(DISCOVERY_PAYLOAD.encode()),
    ],
)
def test_parse_discovery(
    factory: QbusMqttMessageFactory, payload: str | bytes | bytearray
) -> None:
    """Test parsing a discovery payload of any supported payload type."""
    discovery = factory.parse_discovery(payload)

    assert discovery is not None
    assert discovery.name == "abc"
    assert discovery.devices[0].serial_number == "000001"
    assert discovery.devices[0].outputs[0].id == "UL15"


@pytest.mark.parametrize(
    "payload", ['{"app": "abc", "devices": []}', '{"app": "abc"}', "{}"]
)
def test_parse_discovery_without_devices(
    factory: QbusMqttMessageFactory, caplog: pytest.LogCaptureFixture, payload: str
) -> None:
    """Test a discovery payload without devices is rejected."""
    with caplog.at_level(logging.ERROR):
        assert factory.parse_discovery(payload) is None

    assert "Incomplete discovery payload" in caplog.text


def test_parse_gateway_state(factory: QbusMqttMessageFactory) -> None:
    """Test parsing a gateway state payload."""
    state = factory.parse_gateway_state(
        '{"id": "gw", "online": false, "reason": "REASON_CONNECTION_LOST"}'
    )

    assert state is not None
    assert state.id == "gw"
    assert state.online is False
    assert state.reason == "REASON_CONNECTION_LOST"


def test_parse_device_state(factory: QbusMqttMessageFactory) -> None:
    """Test parsing a device state payload."""
    state = factory.parse_device_state(
        '{"id": "UL1", "properties": {"connectable": true, "connected": false}}'
    )

    assert state is not None
    assert state.id == "UL1"
    assert state.properties is not None
    assert state.properties.connectable is True
    assert state.properties.connected is False


def test_parse_output_state(factory: QbusMqttMessageFactory) -> None:
    """Test parsing an output state payload into the requested class."""
    state = factory.parse_output_state(
        QbusMqttOnOffState,
        '{"id": "UL15", "type": "state", "properties": {"value": true}}',
    )

    assert isinstance(state, QbusMqttOnOffState)
    assert state.id == "UL15"
    assert state.type == StateType.STATE
    assert state.read_value() is True


@pytest.mark.parametrize("payload", ["", b"", bytearray()])
def test_deserialize_empty_payload(
    factory: QbusMqttMessageFactory,
    caplog: pytest.LogCaptureFixture,
    payload: str | bytes | bytearray,
) -> None:
    """Test an empty payload results in None."""
    with caplog.at_level(logging.WARNING):
        assert factory.deserialize(QbusMqttState, payload) is None

    assert "Empty state payload for QbusMqttState" in caplog.text


@pytest.mark.parametrize("payload", ["{invalid", b"\xff\xfe\x00"])
def test_deserialize_invalid_payload(
    factory: QbusMqttMessageFactory,
    caplog: pytest.LogCaptureFixture,
    payload: str | bytes,
) -> None:
    """Test an invalid json payload results in None."""
    with caplog.at_level(logging.ERROR):
        assert factory.parse_gateway_state(payload) is None
        assert factory.parse_discovery(payload) is None

    assert "Invalid state payload for QbusMqttGatewayState" in caplog.text
    assert "Invalid state payload for QbusDiscovery" in caplog.text


def test_serialize_ignores_none(factory: QbusMqttMessageFactory) -> None:
    """Test None values are omitted when serializing objects."""
    state = QbusMqttAnalogState(id="UL16", type=StateType.STATE)

    assert json.loads(factory.serialize(state)) == {"id": "UL16", "type": "state"}

    state.write_percentage(42.5)

    assert json.loads(factory.serialize(state)) == {
        "id": "UL16",
        "type": "state",
        "properties": {"value": 42.5},
    }


def test_serialize_unsupported_type(factory: QbusMqttMessageFactory) -> None:
    """Test objects without a __dict__ still raise a TypeError."""
    with pytest.raises(TypeError):
        factory.serialize({1, 2})


def test_create_device_activate_request(
    factory: QbusMqttMessageFactory, device: QbusMqttDevice
) -> None:
    """Test creating a device activation request."""
    request = factory.create_device_activate_request(device)

    assert request.topic == f"{TOPIC_PREFIX}/UL1/setState"
    assert isinstance(request.payload, str)
    assert json.loads(request.payload) == {
        "id": "UL1",
        "type": "action",
        "action": "activate",
        "properties": {"authKey": "ubielite"},
    }


def test_create_device_state_request(
    factory: QbusMqttMessageFactory, device: QbusMqttDevice
) -> None:
    """Test creating a device state request."""
    request = factory.create_device_state_request(device, "custom")

    assert request.topic == "custom/getState"
    assert request.payload == '["UL1"]'


def test_create_state_request(factory: QbusMqttMessageFactory) -> None:
    """Test creating a state request for multiple ids."""
    request = factory.create_state_request(["UL15", "UL16"])

    assert request.topic == f"{TOPIC_PREFIX}/getState"
    assert isinstance(request.payload, str)
    assert json.loads(request.payload) == ["UL15", "UL16"]


def test_create_set_output_state_request(
    factory: QbusMqttMessageFactory, device: QbusMqttDevice
) -> None:
    """Test creating a request to update an output state."""
    state = QbusMqttOnOffState(id="UL15", type=StateType.STATE)
    state.write_value(True)

    request = factory.create_set_output_state_request(device, state)

    assert request.topic == f"{TOPIC_PREFIX}/UL1/UL15/setState"
    assert isinstance(request.payload, str)
    assert json.loads(request.payload) == {
        "id": "UL15",
        "type": "state",
        "properties": {"value": True},
    }


@pytest.mark.parametrize(
    ("method", "args", "expected"),
    [
        ("get_gateway_state_topic", (), "state"),
        ("get_get_config_topic", (), "getConfig"),
        ("get_config_topic", (), "config"),
        ("get_get_state_topic", (), "getState"),
        ("get_device_state_topic", ("UL1",), "UL1/state"),
        ("get_device_command_topic", ("UL1",), "UL1/setState"),
        ("get_output_command_topic", ("UL1", "UL15"), "UL1/UL15/setState"),
        ("get_output_state_topic", ("UL1", "UL15"), "UL1/UL15/state"),
    ],
)
def test_topics(method: str, args: tuple[str, ...], expected: str) -> None:
    """Test topics with the default and a custom prefix."""
    topic_factory = QbusMqttTopicFactory()
    get_topic = getattr(topic_factory, method)

    assert get_topic(*args) == f"{TOPIC_PREFIX}/{expected}"
    assert get_topic(*args, prefix="custom") == f"custom/{expected}"
