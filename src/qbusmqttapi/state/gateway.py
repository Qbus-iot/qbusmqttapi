"""Qbus gateway state model."""

from enum import StrEnum


class GatewayStateKey(StrEnum):
    """Top-level keys to read the gateway state."""

    ID = "id"
    ONLINE = "online"
    REASON = "reason"


class QbusMqttGatewayState:
    """MQTT representation of a Qbus gateway state."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.id: str | None = data.get(GatewayStateKey.ID)
        self.online: bool | None = data.get(GatewayStateKey.ONLINE)
        self.reason: str | None = data.get(GatewayStateKey.REASON)
