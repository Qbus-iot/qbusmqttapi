"""Tests for the gauge state model."""

from qbusmqttapi.state.gauge import GaugeStateProperty, QbusMqttGaugeState


def test_gauge_state() -> None:
    """Test the gauge state."""
    state = QbusMqttGaugeState({"properties": {"currentValue": 1.5}})

    assert state.read_value(GaugeStateProperty.CURRENT_VALUE) == 1.5
    assert state.read_value(GaugeStateProperty.CONSUMPTION_VALUE) == 0
