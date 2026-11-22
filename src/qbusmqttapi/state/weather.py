"""Qbus weather station state model."""

from enum import StrEnum

from .base import QbusMqttState


class WeatherStationStateProperty(StrEnum):
    """Keys to read the weahter station state."""

    DAYLIGHT = "dayLight"
    LIGHT = "light"
    LIGHT_EAST = "lightEast"
    LIGHT_SOUTH = "lightSouth"
    LIGHT_WEST = "lightWest"
    RAINING = "raining"
    TEMPERATURE = "temperature"
    TWILIGHT = "twilight"
    WIND = "wind"


class QbusMqttWeatherState(QbusMqttState):
    """MQTT representation of a Qbus weather station output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_daylight(self) -> float:
        """Read the daylight status of the weather station."""
        return self.read_float_property(WeatherStationStateProperty.DAYLIGHT, 0)

    def read_light(self) -> float:
        """Read the light level of the weather station."""
        return self.read_float_property(WeatherStationStateProperty.LIGHT, 0)

    def read_light_east(self) -> float:
        """Read the east-facing light level of the weather station."""
        return self.read_float_property(WeatherStationStateProperty.LIGHT_EAST, 0)

    def read_light_south(self) -> float:
        """Read the south-facing light level of the weather station."""
        return self.read_float_property(WeatherStationStateProperty.LIGHT_SOUTH, 0)

    def read_light_west(self) -> float:
        """Read the west-facing light level of the weather station."""
        return self.read_float_property(WeatherStationStateProperty.LIGHT_WEST, 0)

    def read_raining(self) -> bool:
        """Read the rain status of the weather station."""
        return self.read_bool_property(WeatherStationStateProperty.RAINING, False)

    def read_temperature(self) -> float:
        """Read the temperature from the weather station."""
        return self.read_float_property(WeatherStationStateProperty.TEMPERATURE, 0)

    def read_twilight(self) -> bool:
        """Read the twilight status of the weather station."""
        return self.read_bool_property(WeatherStationStateProperty.TWILIGHT, False)

    def read_wind(self) -> float:
        """Read the wind speed from the weather station."""
        return self.read_float_property(WeatherStationStateProperty.WIND, 0)
