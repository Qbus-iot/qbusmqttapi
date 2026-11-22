"""Qbus base state model."""

from enum import StrEnum
from typing import Any, overload


class StateType(StrEnum):
    """Values to be used as state type."""

    ACTION = "action"
    EVENT = "event"
    STATE = "state"


class StateAction(StrEnum):
    """Values to be used as state action."""

    ACTIVATE = "activate"
    ACTIVE = "active"


class StateKey(StrEnum):
    """Top-level keys to read or write the state."""

    ACTION = "action"
    ID = "id"
    PROPERTIES = "properties"
    TYPE = "type"


class QbusMqttState:
    """MQTT representation of a Qbus state."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
        action: str | None = None,
    ) -> None:
        """Initialize state."""
        self.id: str = ""
        self.type: str = ""
        self.action: str | None = None
        self.properties: dict | None = None

        if data is not None:
            self.id = data.get(StateKey.ID, "")
            self.type = data.get(StateKey.TYPE, "")
            self.action = data.get(StateKey.ACTION)
            self.properties = data.get(StateKey.PROPERTIES)

        if id is not None:
            self.id = id

        if type is not None:
            self.type = type

        if action is not None:
            self.action = action

    def read_property(self, key: str, default: Any) -> Any:
        """Read a property."""
        return self.properties.get(key, default) if self.properties else default

    @overload
    def read_bool_property(self, key: str, default: bool) -> bool: ...

    @overload
    def read_bool_property(self, key: str, default: None) -> bool | None: ...

    def read_bool_property(self, key: str, default: bool | None) -> bool | None:
        """Read a boolean property, or return the default if missing or not a boolean."""
        value = self.read_property(key, None)
        return value if isinstance(value, bool) else default

    @overload
    def read_float_property(self, key: str, default: float) -> float: ...

    @overload
    def read_float_property(self, key: str, default: None) -> float | None: ...

    def read_float_property(self, key: str, default: float | None) -> float | None:
        """Read a numeric property as float, or return the default if missing or not a number."""
        value = self.read_property(key, None)

        # bool is a subclass of int, but must not be treated as a number.
        if isinstance(value, int | float) and not isinstance(value, bool):
            return float(value)

        return default

    @overload
    def read_int_property(self, key: str, default: int) -> int: ...

    @overload
    def read_int_property(self, key: str, default: None) -> int | None: ...

    def read_int_property(self, key: str, default: int | None) -> int | None:
        """Read an integer property, or return the default if missing or not a whole number."""
        value = self.read_property(key, None)

        if isinstance(value, bool):
            return default

        if isinstance(value, int):
            return value

        if isinstance(value, float) and value.is_integer():
            return int(value)

        return default

    @overload
    def read_str_property(self, key: str, default: str) -> str: ...

    @overload
    def read_str_property(self, key: str, default: None) -> str | None: ...

    def read_str_property(self, key: str, default: str | None) -> str | None:
        """Read a string property, or return the default if missing or not a string."""
        value = self.read_property(key, None)
        return value if isinstance(value, str) else default

    def write_property(self, key: str, value: Any) -> None:
        """Add or update a property."""
        if self.properties is None:
            self.properties = {}

        self.properties[key] = value
