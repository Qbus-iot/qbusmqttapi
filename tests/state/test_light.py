"""Tests for the light state model."""

import pytest

from qbusmqttapi.state.light import MultiColorRegime, QbusMqttMultiColorState


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
    assert state.read_current_regime() is MultiColorRegime.COLOR_WHEEL
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
    state.write_current_regime(MultiColorRegime.MOVIE_SELECT)
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
    assert state.read_current_regime() is MultiColorRegime.MOVIE_SELECT


def test_multicolor_state_invalid_regime() -> None:
    """Test reading an unknown multi-color regime raises."""
    state = QbusMqttMultiColorState({"properties": {"currRegime": "Unknown"}})

    with pytest.raises(ValueError):
        state.read_current_regime()
