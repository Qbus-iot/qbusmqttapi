"""Qbus device state model."""

from enum import StrEnum


class DeviceStateKey(StrEnum):
    """Top-level keys to read the device state."""

    ID = "id"
    PROPERTIES = "properties"


class DeviceStateProperty(StrEnum):
    """Keys to read or write the device state properties."""

    AUTHKEY = "authKey"
    CONNECTABLE = "connectable"
    CONNECTED = "connected"


class QbusMqttDeviceStateProperties:
    """MQTT representation of a Qbus device its state properties."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.connectable: bool | None = data.get(DeviceStateProperty.CONNECTABLE)
        self.connected: bool | None = data.get(DeviceStateProperty.CONNECTED)


class QbusMqttDeviceState:
    """MQTT representation of a Qbus device state."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.id: str | None = data.get(DeviceStateKey.ID)

        properties = data.get(DeviceStateKey.PROPERTIES)
        self.properties: QbusMqttDeviceStateProperties | None = (
            QbusMqttDeviceStateProperties(properties) if properties is not None else None
        )
