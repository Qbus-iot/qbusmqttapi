"""Tests for the weather state model."""

from qbusmqttapi.state.weather import QbusMqttWeatherState


def test_weather_state() -> None:
    """Test the weather station state."""
    state = QbusMqttWeatherState(
        {
            "properties": {
                "dayLight": 1,
                "light": 100,
                "lightEast": 10,
                "lightSouth": 20,
                "lightWest": 30,
                "raining": True,
                "temperature": 12.5,
                "twilight": True,
                "wind": 4.2,
            }
        }
    )

    assert state.read_daylight() == 1
    assert state.read_light() == 100
    assert state.read_light_east() == 10
    assert state.read_light_south() == 20
    assert state.read_light_west() == 30
    assert state.read_raining() is True
    assert state.read_temperature() == 12.5
    assert state.read_twilight() is True
    assert state.read_wind() == 4.2


def test_weather_state_defaults() -> None:
    """Test the weather station state without properties."""
    state = QbusMqttWeatherState()

    assert state.read_daylight() == 0
    assert state.read_light() == 0
    assert state.read_light_east() == 0
    assert state.read_light_south() == 0
    assert state.read_light_west() == 0
    assert state.read_raining() is False
    assert state.read_temperature() == 0
    assert state.read_twilight() is False
    assert state.read_wind() == 0
