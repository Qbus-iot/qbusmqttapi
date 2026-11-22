"""Tests for the on/off state model."""

from qbusmqttapi.state.base import StateType
from qbusmqttapi.state.onoff import QbusMqttOnOffState


def test_onoff_state() -> None:
    """Test the on/off state."""
    state = QbusMqttOnOffState(id="UL15", type=StateType.STATE)

    assert state.read_value() is False

    state.write_value(True)

    assert state.read_value() is True
    assert state.properties == {"value": True}
