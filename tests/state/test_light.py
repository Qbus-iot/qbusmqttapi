"""Tests for the light state model."""

import pytest

from qbusmqttapi.state.light import (
    LightRegime,
    MultiColorRegime,
    QbusMqttMultiColorState,
    QbusMqttWwcwState,
)


def test_multicolor_state() -> None:
    """Test the multi-color state."""
    state = QbusMqttMultiColorState(
        {
            "properties": {
                "brightness": 50,
                "currRegime": "ColorWheel",
                "hue": 120,
                "on": True,
                "presetColor": 2,
                "presetMovie": 3,
                "saturation": 75,
            }
        }
    )

    assert state.read_brightness() == 50
    assert state.read_current_regime() is LightRegime.COLOR_WHEEL
    assert state.read_hue() == 120
    assert state.read_on() is True
    assert state.read_preset_color() == 2
    assert state.read_preset_movie() == 3
    assert state.read_saturation() == 75


def test_multicolor_state_defaults() -> None:
    """Test the multi-color state without properties."""
    state = QbusMqttMultiColorState()

    assert state.read_brightness() is None
    assert state.read_current_regime() is None
    assert state.read_hue() is None
    assert state.read_on() is False
    assert state.read_preset_color() is None
    assert state.read_preset_movie() is None
    assert state.read_saturation() is None


def test_multicolor_state_write() -> None:
    """Test writing the multi-color state."""
    state = QbusMqttMultiColorState()

    state.write_brightness(10)
    state.write_current_regime(LightRegime.MOVIE_SELECT)
    state.write_hue(200)
    state.write_on(True)
    state.write_preset_color(4)
    state.write_preset_movie(5)
    state.write_saturation(30)

    assert state.properties == {
        "brightness": 10,
        "currRegime": "MovieSelect",
        "hue": 200,
        "on": True,
        "presetColor": 4,
        "presetMovie": 5,
        "saturation": 30,
    }
    assert state.read_current_regime() is LightRegime.MOVIE_SELECT


def test_multicolor_state_invalid_regime() -> None:
    """Test reading an unknown multi-color regime raises."""
    state = QbusMqttMultiColorState({"properties": {"currRegime": "Unknown"}})

    with pytest.raises(ValueError):
        state.read_current_regime()


def test_wwcw_state() -> None:
    """Test the WWCW state."""
    state = QbusMqttWwcwState(
        {
            "id": "UL9",
            "properties": {
                "brightness": 61.176470588235297,
                "currRegime": "ColorSelect",
                "on": True,
                "presetColor": 2,
                "presetMovie": -1,
                "temperature": 100,
            },
            "type": "state",
        }
    )

    assert state.id == "UL9"
    assert state.type == "state"
    assert state.read_brightness() == pytest.approx(61.176470588235297)
    assert state.read_current_regime() is LightRegime.COLOR_SELECT
    assert state.read_on() is True
    assert state.read_preset_color() == 2
    assert state.read_preset_movie() == -1
    assert state.read_temperature() == 100


def test_wwcw_state_defaults() -> None:
    """Test the WWCW state without properties."""
    state = QbusMqttWwcwState()

    assert state.read_brightness() is None
    assert state.read_current_regime() is None
    assert state.read_on() is False
    assert state.read_preset_color() is None
    assert state.read_preset_movie() is None
    assert state.read_temperature() is None


def test_wwcw_state_write() -> None:
    """Test writing the WWCW state."""
    state = QbusMqttWwcwState(id="UL9", type="state")

    state.write_brightness(10)
    state.write_current_regime(LightRegime.MOVIE_SELECT)
    state.write_on(True)
    state.write_preset_color(4)
    state.write_preset_movie(1)
    state.write_temperature(33.3)

    assert state.properties == {
        "brightness": 10,
        "currRegime": "MovieSelect",
        "on": True,
        "presetColor": 4,
        "presetMovie": 1,
        "temperature": 33.3,
    }
    assert state.read_current_regime() is LightRegime.MOVIE_SELECT


def test_wwcw_state_invalid_regime() -> None:
    """Test reading an unknown WWCW regime raises."""
    state = QbusMqttWwcwState({"properties": {"currRegime": "Unknown"}})

    with pytest.raises(ValueError):
        state.read_current_regime()


def test_multicolor_regime_deprecated_alias() -> None:
    """Test the deprecated MultiColorRegime alias still resolves to LightRegime."""
    state = QbusMqttMultiColorState({"properties": {"currRegime": "ColorSelect"}})

    assert state.read_current_regime() is MultiColorRegime.COLOR_SELECT
