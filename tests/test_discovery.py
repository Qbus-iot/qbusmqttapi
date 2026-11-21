"""Tests for the discovery models."""

import pytest

from qbusmqttapi.discovery import QbusDiscovery, QbusMqttDevice, QbusMqttOutput

OUTPUT_DATA = {
    "id": "UL15",
    "type": "onoff",
    "name": "Kitchen",
    "refId": "000001/10",
    "properties": {"value": {"type": "boolean"}},
    "actions": {"toggle": None},
    "location": "Ground floor",
    "locationId": 3,
    "variant": "",
}

DEVICE_DATA = {
    "id": "UL1",
    "ip": "192.168.1.10",
    "mac": "00:11:22:33:44:55",
    "name": "CTD 3.0",
    "serialNr": "000001",
    "type": "Qbus",
    "version": "3.14.0",
    "functionBlocks": [
        OUTPUT_DATA,
        {"id": "UL16", "type": "analog", "name": "Living"},
    ],
}


@pytest.fixture
def device() -> QbusMqttDevice:
    """Return a device."""
    return QbusMqttDevice(DEVICE_DATA)


def test_device_properties(device: QbusMqttDevice) -> None:
    """Test reading device properties."""
    assert device.id == "UL1"
    assert device.ip == "192.168.1.10"
    assert device.mac == "00:11:22:33:44:55"
    assert device.name == "CTD 3.0"
    assert device.serial_number == "000001"
    assert device.type == "Qbus"
    assert device.version == "3.14.0"


def test_device_defaults() -> None:
    """Test missing or null device values fall back to defaults."""
    device = QbusMqttDevice({"id": None})

    assert device.id == ""
    assert device.ip == ""
    assert device.mac == ""
    assert device.name == ""
    assert device.serial_number == ""
    assert device.type == ""
    assert device.version == ""
    assert device.outputs == []


def test_device_outputs(device: QbusMqttDevice) -> None:
    """Test outputs are created from function blocks and linked to the device."""
    outputs = device.outputs

    assert [x.id for x in outputs] == ["UL15", "UL16"]
    assert all(x.device is device for x in outputs)


def test_output_properties(device: QbusMqttDevice) -> None:
    """Test reading output properties."""
    output = QbusMqttOutput(OUTPUT_DATA, device)

    assert output.id == "UL15"
    assert output.type == "onoff"
    assert output.name == "Kitchen"
    assert output.ref_id == "000001/10"
    assert output.properties == {"value": {"type": "boolean"}}
    assert output.actions == {"toggle": None}
    assert output.location == "Ground floor"
    assert output.location_id == 3
    assert output.device is device


def test_output_defaults(device: QbusMqttDevice) -> None:
    """Test missing or null output values fall back to defaults."""
    output = QbusMqttOutput({"properties": None, "actions": None}, device)

    assert output.id == ""
    assert output.type == ""
    assert output.name == ""
    assert output.ref_id == ""
    assert output.properties == {}
    assert output.actions == {}
    assert output.location == ""
    assert output.location_id == 0
    assert output.variant == ""


@pytest.mark.parametrize(
    ("variant", "expected"),
    [
        ("dimmer", "dimmer"),
        (None, ""),
        (["a", None, "b"], ["a", "b"]),
        (("a", None), ["a"]),
        ([None], []),
    ],
)
def test_output_variant(
    device: QbusMqttDevice, variant: object, expected: object
) -> None:
    """Test the variant drops None values from sequences."""
    output = QbusMqttOutput({"variant": variant}, device)

    assert output.variant == expected


def test_discovery() -> None:
    """Test discovery creates devices and reads the app name."""
    discovery = QbusDiscovery(
        {"app": "abc", "devices": [DEVICE_DATA, {"id": "UL2", "serialNr": "000002"}]}
    )

    assert discovery.name == "abc"
    assert [x.id for x in discovery.devices] == ["UL1", "UL2"]


@pytest.mark.parametrize("data", [{}, {"app": None, "devices": None}])
def test_discovery_missing_values(data: dict) -> None:
    """Test missing app and devices fall back to defaults."""
    discovery = QbusDiscovery(data)

    assert discovery.name == ""
    assert discovery.devices == []


@pytest.mark.parametrize("device_id", ["UL2", "ul2"])
def test_discovery_get_device_by_id(device_id: str) -> None:
    """Test finding a device by id is case-insensitive."""
    discovery = QbusDiscovery({"app": "abc", "devices": [DEVICE_DATA, {"id": "UL2"}]})

    device = discovery.get_device_by_id(device_id)

    assert device is not None
    assert device.id == "UL2"


def test_discovery_get_device_by_id_not_found() -> None:
    """Test finding an unknown device by id returns None."""
    discovery = QbusDiscovery({"app": "abc", "devices": [DEVICE_DATA]})

    assert discovery.get_device_by_id("UL99") is None


@pytest.mark.parametrize("serial", ["ABC123", "abc123"])
def test_discovery_get_device_by_serial(serial: str) -> None:
    """Test finding a device by serial number is case-insensitive."""
    discovery = QbusDiscovery(
        {"app": "abc", "devices": [DEVICE_DATA, {"id": "UL2", "serialNr": "Abc123"}]}
    )

    device = discovery.get_device_by_serial(serial)

    assert device is not None
    assert device.id == "UL2"


def test_discovery_get_device_by_serial_not_found() -> None:
    """Test finding an unknown device by serial number returns None."""
    discovery = QbusDiscovery({"app": "abc", "devices": [DEVICE_DATA]})

    assert discovery.get_device_by_serial("999999") is None
