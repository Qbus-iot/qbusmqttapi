"""Tests for the humidity state model."""

from qbusmqttapi.state.humidity import QbusMqttHumidityState


def test_humidity_state() -> None:
    """Test the humidity state."""
    state = QbusMqttHumidityState({"properties": {"value": 55.5, "currRegime": "AUTO"}})

    assert state.read_value() == 55.5
    assert state.read_regime() == "AUTO"

    state.write_regime("MANUAL")

    assert state.read_regime() == "MANUAL"


def test_humidity_state_defaults() -> None:
    """Test the humidity state without properties."""
    state = QbusMqttHumidityState()

    assert state.read_value() == 0
    assert state.read_regime() is None
