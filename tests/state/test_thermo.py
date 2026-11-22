"""Tests for the thermo state model."""

from qbusmqttapi.state.thermo import QbusMqttThermoState


def test_thermo_state() -> None:
    """Test the thermo state."""
    state = QbusMqttThermoState(
        {"properties": {"currTemp": 20.5, "setTemp": 21, "currRegime": "COMFORT"}}
    )

    assert state.read_current_temperature() == 20.5
    assert state.read_set_temperature() == 21
    assert state.read_regime() == "COMFORT"

    state.write_set_temperature(22.5)
    state.write_regime("NIGHT")

    assert state.read_set_temperature() == 22.5
    assert state.read_regime() == "NIGHT"


def test_thermo_state_defaults() -> None:
    """Test the thermo state without properties."""
    state = QbusMqttThermoState()

    assert state.read_current_temperature() is None
    assert state.read_set_temperature() is None
    assert state.read_regime() is None
