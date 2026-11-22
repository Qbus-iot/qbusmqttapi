"""Tests for the stepper state model."""

from qbusmqttapi.state.stepper import QbusMqttStepperState


def test_stepper_state() -> None:
    """Test the stepper state."""
    state = QbusMqttStepperState()

    assert state.read_value() is None

    state.write_value(3)

    assert state.read_value() == 3
    assert state.properties == {"value": 3}
