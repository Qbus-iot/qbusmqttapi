"""Tests for the base state model."""

import pytest

from qbusmqttapi.state.base import QbusMqttState, StateAction, StateType


def test_state_from_data() -> None:
    """Test a state created from data."""
    state = QbusMqttState(
        {"id": "UL15", "type": "event", "action": "active", "properties": {"value": 1}}
    )

    assert state.id == "UL15"
    assert state.type == StateType.EVENT
    assert state.action == StateAction.ACTIVE
    assert state.properties == {"value": 1}


def test_state_defaults() -> None:
    """Test a state without data or arguments."""
    for state in (QbusMqttState(), QbusMqttState({})):
        assert state.id == ""
        assert state.type == ""
        assert state.action is None
        assert state.properties is None


def test_state_arguments_override_data() -> None:
    """Test keyword arguments take precedence over data."""
    state = QbusMqttState(
        {"id": "UL15", "type": "event", "action": "active", "properties": {"value": 1}},
        id="UL16",
        type=StateType.ACTION,
        action=StateAction.ACTIVATE,
    )

    assert state.id == "UL16"
    assert state.type == StateType.ACTION
    assert state.action == StateAction.ACTIVATE
    assert state.properties == {"value": 1}


def test_state_read_property() -> None:
    """Test reading properties falls back to the default."""
    assert QbusMqttState().read_property("value", "default") == "default"
    assert (
        QbusMqttState({"properties": {}}).read_property("value", "default") == "default"
    )

    state = QbusMqttState({"properties": {"value": 0}})

    assert state.read_property("value", "default") == 0
    assert state.read_property("other", "default") == "default"


@pytest.mark.parametrize(
    ("value", "expected"),
    [(True, True), (False, False), (1, None), ("true", None)],
)
def test_state_read_bool_property(value: object, expected: bool | None) -> None:
    """Test reading a boolean property only accepts booleans."""
    state = QbusMqttState({"properties": {"value": value}})

    assert state.read_bool_property("value", None) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(21, 21.0), (21.5, 21.5), (0, 0.0), (True, None), ("21", None)],
)
def test_state_read_float_property(value: object, expected: float | None) -> None:
    """Test reading a float property converts numbers and rejects other types."""
    state = QbusMqttState({"properties": {"value": value}})
    result = state.read_float_property("value", None)

    assert result == expected
    assert type(result) is type(expected)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(50, 50), (50.0, 50), (50.5, None), (True, None), ("50", None)],
)
def test_state_read_int_property(value: object, expected: int | None) -> None:
    """Test reading an int property accepts whole numbers and rejects other types."""
    state = QbusMqttState({"properties": {"value": value}})
    result = state.read_int_property("value", None)

    assert result == expected
    assert type(result) is type(expected)


@pytest.mark.parametrize(("value", "expected"), [("Comfort", "Comfort"), (5, None)])
def test_state_read_str_property(value: object, expected: str | None) -> None:
    """Test reading a string property only accepts strings."""
    state = QbusMqttState({"properties": {"value": value}})

    assert state.read_str_property("value", None) == expected


def test_state_read_typed_property_default() -> None:
    """Test typed property readers return the default when the property is missing."""
    state = QbusMqttState()

    assert state.read_bool_property("value", False) is False
    assert state.read_float_property("value", 1.5) == 1.5
    assert state.read_int_property("value", 3) == 3
    assert state.read_str_property("value", "x") == "x"


def test_state_write_property() -> None:
    """Test writing properties creates and updates the properties."""
    state = QbusMqttState()

    state.write_property("value", 1)
    state.write_property("other", 2)
    state.write_property("value", 3)

    assert state.properties == {"value": 3, "other": 2}
