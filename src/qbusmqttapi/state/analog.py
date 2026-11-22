"""Qbus analog state model."""

from enum import StrEnum

from .base import QbusMqttState


class AnalogStateProperty(StrEnum):
    """Keys to read or write the analog state."""

    VALUE = "value"


class QbusMqttAnalogState(QbusMqttState):
    """MQTT representation of a Qbus analog output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_percentage(self) -> float | None:
        """Read the value of the Qbus output."""
        return self.read_float_property(AnalogStateProperty.VALUE, None)

    def write_percentage(self, percentage: float) -> None:
        """Set the value of the Qbus output."""
        self.write_property(AnalogStateProperty.VALUE, percentage)

    def write_on_off(self, on: bool) -> None:
        """Set the Qbus output on or off."""
        self.action = "on" if on else "off"
