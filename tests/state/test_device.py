"""Tests for the device state model."""

from qbusmqttapi.state.device import QbusMqttDeviceState


def test_device_state() -> None:
    """Test the device state with properties."""
    state = QbusMqttDeviceState(
        {"id": "UL1", "properties": {"connectable": False, "connected": True}}
    )

    assert state.id == "UL1"
    assert state.properties is not None
    assert state.properties.connectable is False
    assert state.properties.connected is True


def test_device_state_without_properties() -> None:
    """Test the device state without properties."""
    state = QbusMqttDeviceState({"id": "UL1"})

    assert state.id == "UL1"
    assert state.properties is None
