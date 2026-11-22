"""Qbus gauge state model."""

from enum import StrEnum

from .base import QbusMqttState


class GaugeStateProperty(StrEnum):
    """Keys to read gauge state."""

    CURRENT_VALUE = "currentValue"
    CONSUMPTION_VALUE = "consumptionValue"


class QbusMqttGaugeState(QbusMqttState):
    """MQTT representation of a Qbus gauge output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_value(self, key: GaugeStateProperty) -> float:
        """Read the value of the Qbus output."""
        return self.read_float_property(key, 0)
