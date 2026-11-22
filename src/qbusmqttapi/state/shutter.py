"""Qbus shutter state model."""

from enum import StrEnum

from .base import QbusMqttState


class ShutterStateProperty(StrEnum):
    """Keys to read or write the shutter state."""

    SHUTTER_POSITION = "shutterPosition"
    SLAT_POSITION = "slatPosition"
    STATE = "state"


class QbusMqttShutterState(QbusMqttState):
    """MQTT representation of a Qbus shutter output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_state(self) -> str | None:
        """Read the state of the Qbus output."""
        return self.read_str_property(ShutterStateProperty.STATE, None)

    def write_state(self, state: str) -> None:
        """Set the state of the Qbus output."""
        self.write_property(ShutterStateProperty.STATE, state)

    def read_position(self) -> int | None:
        """Read the position of the Qbus output."""
        return self.read_int_property(ShutterStateProperty.SHUTTER_POSITION, None)

    def write_position(self, percentage: int) -> None:
        """Set the position of the Qbus output."""
        self.write_property(ShutterStateProperty.SHUTTER_POSITION, percentage)

    def read_slat_position(self) -> int | None:
        """Read the slat position of the Qbus output."""
        return self.read_int_property(ShutterStateProperty.SLAT_POSITION, None)

    def write_slat_position(self, percentage: int) -> None:
        """Set the slat position of the Qbus output."""
        self.write_property(ShutterStateProperty.SLAT_POSITION, percentage)
