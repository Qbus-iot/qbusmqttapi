"""Tests for the ventilation state model."""

from qbusmqttapi.state.ventilation import QbusMqttVentilationState


def test_ventilation_state() -> None:
    """Test the ventilation state."""
    state = QbusMqttVentilationState(
        {"properties": {"co2": 650.5, "refresh": 2, "currRegime": "AUTO"}}
    )

    assert state.read_co2() == 650.5
    assert state.read_refresh() == 2
    assert state.read_regime() == "AUTO"

    state.write_regime("MANUAL")

    assert state.read_regime() == "MANUAL"


def test_ventilation_state_defaults() -> None:
    """Test the ventilation state without properties."""
    state = QbusMqttVentilationState()

    assert state.read_co2() == 0
    assert state.read_refresh() == 0
    assert state.read_regime() is None
