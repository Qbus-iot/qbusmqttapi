"""Tests for the analog state model."""

import pytest

from qbusmqttapi.state.analog import QbusMqttAnalogState


def test_analog_state() -> None:
    """Test the analog state."""
    state = QbusMqttAnalogState({"properties": {"value": 25.5}})

    assert state.read_percentage() == 25.5

    state.write_percentage(80)

    assert state.read_percentage() == 80
    assert QbusMqttAnalogState().read_percentage() is None


@pytest.mark.parametrize(("on", "action"), [(True, "on"), (False, "off")])
def test_analog_state_write_on_off(on: bool, action: str) -> None:
    """Test switching the analog output on or off sets the action."""
    state = QbusMqttAnalogState(id="UL16")

    state.write_on_off(on)

    assert state.action == action
    assert state.properties is None
