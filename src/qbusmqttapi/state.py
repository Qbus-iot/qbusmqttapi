"""Qbus state models."""

from enum import StrEnum
from typing import Any

# Deprecated: use DeviceStateKey, DeviceStateProperty or GatewayStateKey instead.
# Kept for backwards compatibility and will be removed in a future version.
KEY_DEVICE_CONNECTABLE = "connectable"
KEY_DEVICE_CONNECTED = "connected"
KEY_DEVICE_ID = "id"
KEY_DEVICE_STATE_PROPERTIES = "properties"

KEY_GATEWAY_ID = "id"
KEY_GATEWAY_ONLINE = "online"
KEY_GATEWAY_REASON = "reason"


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


class GatewayStateKey(StrEnum):
    """Top-level keys to read the gateway state."""

    ID = "id"
    ONLINE = "online"
    REASON = "reason"


class DeviceStateKey(StrEnum):
    """Top-level keys to read the device state."""

    ID = "id"
    PROPERTIES = "properties"


class DeviceStateProperty(StrEnum):
    """Keys to read or write the device state properties."""

    AUTHKEY = "authKey"
    CONNECTABLE = "connectable"
    CONNECTED = "connected"


class OnOffStateProperty(StrEnum):
    """Keys to read or write the on/off state."""

    VALUE = "value"


class AnalogStateProperty(StrEnum):
    """Keys to read or write the analog state."""

    VALUE = "value"


class ShutterStateProperty(StrEnum):
    """Keys to read or write the shutter state."""

    SHUTTER_POSITION = "shutterPosition"
    SLAT_POSITION = "slatPosition"
    STATE = "state"


class ThermoStateProperty(StrEnum):
    """Keys to read or write the thermo state."""

    CURRENT_REGIME = "currRegime"
    CURRENT_TEMPERATURE = "currTemp"
    SET_TEMPERATURE = "setTemp"


class VentilationStateProperty(StrEnum):
    """Keys to read or write the ventilation state."""

    CO2 = "co2"
    CURRENT_REGIME = "currRegime"
    REFRESH = "refresh"


class HumidityStateProperty(StrEnum):
    """Keys to read or write the humidity state."""

    CURRENT_REGIME = "currRegime"
    VALUE = "value"


class StepperStateProperty(StrEnum):
    """Keys to read or write the stepper state."""

    VALUE = "value"


class GaugeStateProperty(StrEnum):
    """Keys to read gauge state."""

    CURRENT_VALUE = "currentValue"
    CONSUMPTION_VALUE = "consumptionValue"


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


class MultiColorStateProperty(StrEnum):
    """Keys to read or write the multi-color state."""

    BRIGHTNESS = "brightness"
    CURRENT_REGIME = "currRegime"
    HUE = "hue"
    ON = "on"
    PRESET_COLOR = "presetColor"
    PRESET_MOVIE = "presetMovie"
    SATURATION = "saturation"


class MultiColorRegime(StrEnum):
    """Possible regimes for the multi-color output."""

    COLOR_SELECT = "ColorSelect"
    COLOR_WHEEL = "ColorWheel"
    MOVIE_SELECT = "MovieSelect"


class QbusMqttGatewayState:
    """MQTT representation of a Qbus gateway state."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.id: str | None = data.get(GatewayStateKey.ID)
        self.online: bool | None = data.get(GatewayStateKey.ONLINE)
        self.reason: str | None = data.get(GatewayStateKey.REASON)


class QbusMqttDeviceStateProperties:
    """MQTT representation of a Qbus device its state properties."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.connectable: bool | None = data.get(DeviceStateProperty.CONNECTABLE)
        self.connected: bool | None = data.get(DeviceStateProperty.CONNECTED)


class QbusMqttDeviceState:
    """MQTT representation of a Qbus device state."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.id: str | None = data.get(DeviceStateKey.ID)

        properties = data.get(DeviceStateKey.PROPERTIES)
        self.properties: QbusMqttDeviceStateProperties | None = (
            QbusMqttDeviceStateProperties(properties) if properties is not None else None
        )


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

    def write_property(self, key: str, value: Any) -> None:
        """Add or update a property."""
        if self.properties is None:
            self.properties = {}

        self.properties[key] = value


class QbusMqttOnOffState(QbusMqttState):
    """MQTT representation of a Qbus on/off output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_value(self) -> bool:
        """Read the value of the Qbus output."""
        return self.read_property(OnOffStateProperty.VALUE, False)

    def write_value(self, on: bool) -> None:
        """Set the Qbus output on or off."""
        self.write_property(OnOffStateProperty.VALUE, on)


class QbusMqttAnalogState(QbusMqttState):
    """MQTT representation of a Qbus analog output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_percentage(self) -> float | None:
        """Read the value of the Qbus output."""
        return self.read_property(AnalogStateProperty.VALUE, None)

    def write_percentage(self, percentage: float) -> None:
        """Set the value of the Qbus output."""
        self.write_property(AnalogStateProperty.VALUE, percentage)

    def write_on_off(self, on: bool) -> None:
        """Set the Qbus output on or off."""
        self.action = "on" if on else "off"


class QbusMqttShutterState(QbusMqttState):
    """MQTT representation of a Qbus shutter output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_state(self) -> str | None:
        """Read the state of the Qbus output."""
        return self.read_property(ShutterStateProperty.STATE, None)

    def write_state(self, state: str) -> None:
        """Set the state of the Qbus output."""
        self.write_property(ShutterStateProperty.STATE, state)

    def read_position(self) -> int | None:
        """Read the position of the Qbus output."""
        return self.read_property(ShutterStateProperty.SHUTTER_POSITION, None)

    def write_position(self, percentage: int) -> None:
        """Set the position of the Qbus output."""
        self.write_property(ShutterStateProperty.SHUTTER_POSITION, percentage)

    def read_slat_position(self) -> int | None:
        """Read the slat position of the Qbus output."""
        return self.read_property(ShutterStateProperty.SLAT_POSITION, None)

    def write_slat_position(self, percentage: int) -> None:
        """Set the slat position of the Qbus output."""
        self.write_property(ShutterStateProperty.SLAT_POSITION, percentage)


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
        return self.read_property(ThermoStateProperty.CURRENT_TEMPERATURE, None)

    def read_set_temperature(self) -> float | None:
        """Read the set temperature of the Qbus output."""
        return self.read_property(ThermoStateProperty.SET_TEMPERATURE, None)

    def write_set_temperature(self, temperature: float) -> None:
        """Set the set temperature of the Qbus output."""
        self.write_property(ThermoStateProperty.SET_TEMPERATURE, temperature)

    def read_regime(self) -> str | None:
        """Read the regime of the Qbus output."""
        return self.read_property(ThermoStateProperty.CURRENT_REGIME, None)

    def write_regime(self, regime: str) -> None:
        """Set the regime of the Qbus output."""
        self.write_property(ThermoStateProperty.CURRENT_REGIME, regime)


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
        return self.read_property(key, 0)


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
        return self.read_property(VentilationStateProperty.CO2, 0)

    def read_refresh(self) -> int:
        """Read the co2 of the Qbus output."""
        return self.read_property(VentilationStateProperty.REFRESH, 0)

    def read_regime(self) -> str | None:
        """Read the regime of the Qbus output."""
        return self.read_property(VentilationStateProperty.CURRENT_REGIME, None)

    def write_regime(self, regime: str) -> None:
        """Set the regime of the Qbus output."""
        self.write_property(VentilationStateProperty.CURRENT_REGIME, regime)


class QbusMqttHumidityState(QbusMqttState):
    """MQTT representation of a Qbus humidity output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_value(self) -> float:
        """Read the value of the Qbus output."""
        return self.read_property(HumidityStateProperty.VALUE, 0)

    def read_regime(self) -> str | None:
        """Read the regime of the Qbus output."""
        return self.read_property(HumidityStateProperty.CURRENT_REGIME, None)

    def write_regime(self, regime: str) -> None:
        """Set the regime of the Qbus output."""
        self.write_property(HumidityStateProperty.CURRENT_REGIME, regime)


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
        return self.read_property(WeatherStationStateProperty.DAYLIGHT, 0)

    def read_light(self) -> float:
        """Read the light level of the weather station."""
        return self.read_property(WeatherStationStateProperty.LIGHT, 0)

    def read_light_east(self) -> float:
        """Read the east-facing light level of the weather station."""
        return self.read_property(WeatherStationStateProperty.LIGHT_EAST, 0)

    def read_light_south(self) -> float:
        """Read the south-facing light level of the weather station."""
        return self.read_property(WeatherStationStateProperty.LIGHT_SOUTH, 0)

    def read_light_west(self) -> float:
        """Read the west-facing light level of the weather station."""
        return self.read_property(WeatherStationStateProperty.LIGHT_WEST, 0)

    def read_raining(self) -> bool:
        """Read the rain status of the weather station."""
        return self.read_property(WeatherStationStateProperty.RAINING, False)

    def read_temperature(self) -> float:
        """Read the temperature from the weather station."""
        return self.read_property(WeatherStationStateProperty.TEMPERATURE, 0)

    def read_twilight(self) -> bool:
        """Read the twilight status of the weather station."""
        return self.read_property(WeatherStationStateProperty.TWILIGHT, False)

    def read_wind(self) -> float:
        """Read the wind speed from the weather station."""
        return self.read_property(WeatherStationStateProperty.WIND, 0)


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
        return self.read_property(StepperStateProperty.VALUE, None)

    def write_value(self, value: int) -> None:
        """Set the value of the Qbus output."""
        self.write_property(StepperStateProperty.VALUE, value)


class QbusMqttMultiColorState(QbusMqttState):
    """MQTT representation of a Qbus multi-color output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        """Initialize state."""
        super().__init__(data, id=id, type=type)

    def read_brightness(self) -> float | None:
        """Read the brightness of the Qbus output."""
        return self.read_property(MultiColorStateProperty.BRIGHTNESS, None)

    def write_brightness(self, value: float) -> None:
        """Set the brightness of the Qbus output."""
        self.write_property(MultiColorStateProperty.BRIGHTNESS, value)

    def read_current_regime(self) -> MultiColorRegime | None:
        """Read the current regime of the Qbus output."""
        value = self.read_property(MultiColorStateProperty.CURRENT_REGIME, None)
        return MultiColorRegime(value) if value is not None else None

    def write_current_regime(self, value: MultiColorRegime) -> None:
        """Set the current regime of the Qbus output."""
        self.write_property(MultiColorStateProperty.CURRENT_REGIME, value.value)

    def read_hue(self) -> float | None:
        """Read the hue of the Qbus output."""
        return self.read_property(MultiColorStateProperty.HUE, None)

    def write_hue(self, value: float) -> None:
        """Set the hue of the Qbus output."""
        self.write_property(MultiColorStateProperty.HUE, value)

    def read_on(self) -> bool:
        """Read the on/off state of the Qbus output."""
        return self.read_property(MultiColorStateProperty.ON, False)

    def write_on(self, value: bool) -> None:
        """Set the Qbus output on or off."""
        self.write_property(MultiColorStateProperty.ON, value)

    def read_preset_color(self) -> int | None:
        """Read the preset color of the Qbus output."""
        return self.read_property(MultiColorStateProperty.PRESET_COLOR, None)

    def write_preset_color(self, value: int) -> None:
        """Set the preset color of the Qbus output."""
        self.write_property(MultiColorStateProperty.PRESET_COLOR, value)

    def read_preset_movie(self) -> int | None:
        """Read the preset movie of the Qbus output."""
        return self.read_property(MultiColorStateProperty.PRESET_MOVIE, None)

    def write_preset_movie(self, value: int) -> None:
        """Set the preset movie of the Qbus output."""
        self.write_property(MultiColorStateProperty.PRESET_MOVIE, value)

    def read_saturation(self) -> float | None:
        """Read the saturation of the Qbus output."""
        return self.read_property(MultiColorStateProperty.SATURATION, None)

    def write_saturation(self, value: float) -> None:
        """Set the saturation of the Qbus output."""
        self.write_property(MultiColorStateProperty.SATURATION, value)
