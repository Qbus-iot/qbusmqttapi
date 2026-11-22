"""Qbus stepper state model."""

from enum import StrEnum

from .base import QbusMqttState


class StepperStateProperty(StrEnum):
    """Keys to read or write the stepper state."""

    VALUE = "value"


class QbusMqttStepperState(QbusMqttState):
    """MQTT representation of a Qbus stepper output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_value(self) -> int | None:
        """Read the value of the Qbus output."""
        return self.read_int_property(StepperStateProperty.VALUE, None)

    def write_value(self, value: int) -> None:
        """Set the value of the Qbus output."""
        self.write_property(StepperStateProperty.VALUE, value)
