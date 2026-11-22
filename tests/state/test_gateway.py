"""Tests for the gateway state model."""

from qbusmqttapi.state.gateway import QbusMqttGatewayState


def test_gateway_state() -> None:
    """Test the gateway state."""
    state = QbusMqttGatewayState({"id": "gw", "online": True, "reason": None})

    assert state.id == "gw"
    assert state.online is True
    assert state.reason is None


def test_gateway_state_empty() -> None:
    """Test the gateway state with missing values."""
    state = QbusMqttGatewayState({})

    assert state.id is None
    assert state.online is None
    assert state.reason is None
