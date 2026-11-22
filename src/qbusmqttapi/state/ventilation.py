"""Qbus HVAC state models."""

from enum import StrEnum

from .base import QbusMqttState


class VentilationStateProperty(StrEnum):
    """Keys to read or write the ventilation state."""

    CO2 = "co2"
    CURRENT_REGIME = "currRegime"
    REFRESH = "refresh"


class QbusMqttVentilationState(QbusMqttState):
    """MQTT representation of a Qbus ventilation output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_co2(self) -> float:
        """Read the co2 of the Qbus output."""
        return self.read_float_property(VentilationStateProperty.CO2, 0)

    def read_refresh(self) -> int:
        """Read the co2 of the Qbus output."""
        return self.read_int_property(VentilationStateProperty.REFRESH, 0)

    def read_regime(self) -> str | None:
        """Read the regime of the Qbus output."""
        return self.read_str_property(VentilationStateProperty.CURRENT_REGIME, None)

    def write_regime(self, regime: str) -> None:
        """Set the regime of the Qbus output."""
        self.write_property(VentilationStateProperty.CURRENT_REGIME, regime)
