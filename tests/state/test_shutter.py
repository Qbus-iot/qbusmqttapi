"""Tests for the shutter state model."""

from qbusmqttapi.state.shutter import QbusMqttShutterState


def test_shutter_state() -> None:
    """Test the shutter state."""
    state = QbusMqttShutterState()

    assert state.read_state() is None
    assert state.read_position() is None
    assert state.read_slat_position() is None

    state.write_state("up")
    state.write_position(40)
    state.write_slat_position(60)

    assert state.read_state() == "up"
    assert state.read_position() == 40
    assert state.read_slat_position() == 60
    assert state.properties == {
        "state": "up",
        "shutterPosition": 40,
        "slatPosition": 60,
    }
