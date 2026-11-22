"""Qbus thermo state model."""

from enum import StrEnum

from .base import QbusMqttState


class ThermoStateProperty(StrEnum):
    """Keys to read or write the thermo state."""

    CURRENT_REGIME = "currRegime"
    CURRENT_TEMPERATURE = "currTemp"
    SET_TEMPERATURE = "setTemp"


class QbusMqttThermoState(QbusMqttState):
    """MQTT representation of a Qbus thermo output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_current_temperature(self) -> float | None:
        """Read the current temperature of the Qbus output."""
        return self.read_float_property(ThermoStateProperty.CURRENT_TEMPERATURE, None)

    def read_set_temperature(self) -> float | None:
        """Read the set temperature of the Qbus output."""
        return self.read_float_property(ThermoStateProperty.SET_TEMPERATURE, None)

    def write_set_temperature(self, temperature: float) -> None:
        """Set the set temperature of the Qbus output."""
        self.write_property(ThermoStateProperty.SET_TEMPERATURE, temperature)

    def read_regime(self) -> str | None:
        """Read the regime of the Qbus output."""
        return self.read_str_property(ThermoStateProperty.CURRENT_REGIME, None)

    def write_regime(self, regime: str) -> None:
        """Set the regime of the Qbus output."""
        self.write_property(ThermoStateProperty.CURRENT_REGIME, regime)
