"""Qbus on/off state model."""

from enum import StrEnum

from .base import QbusMqttState


class OnOffStateProperty(StrEnum):
    """Keys to read or write the on/off state."""

    VALUE = "value"


class QbusMqttOnOffState(QbusMqttState):
    """MQTT representation of a Qbus on/off output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_value(self) -> bool:
        """Read the value of the Qbus output."""
        return self.read_bool_property(OnOffStateProperty.VALUE, False)

    def write_value(self, on: bool) -> None:
        """Set the Qbus output on or off."""
        self.write_property(OnOffStateProperty.VALUE, on)
