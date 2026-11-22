"""Qbus HVAC state models."""

from enum import StrEnum

from .base import QbusMqttState


class HumidityStateProperty(StrEnum):
    """Keys to read or write the humidity state."""

    CURRENT_REGIME = "currRegime"
    VALUE = "value"


class QbusMqttHumidityState(QbusMqttState):
    """MQTT representation of a Qbus humidity output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_value(self) -> float:
        """Read the value of the Qbus output."""
        return self.read_float_property(HumidityStateProperty.VALUE, 0)

    def read_regime(self) -> str | None:
        """Read the regime of the Qbus output."""
        return self.read_str_property(HumidityStateProperty.CURRENT_REGIME, None)

    def write_regime(self, regime: str) -> None:
        """Set the regime of the Qbus output."""
        self.write_property(HumidityStateProperty.CURRENT_REGIME, regime)
