"""Qbus light state models."""

from enum import StrEnum

from .base import QbusMqttState


class MultiColorStateProperty(StrEnum):
    """Keys to read or write the multi-color state."""

    BRIGHTNESS = "brightness"
    CURRENT_REGIME = "currRegime"
    HUE = "hue"
    ON = "on"
    PRESET_COLOR = "presetColor"
    PRESET_MOVIE = "presetMovie"
    SATURATION = "saturation"


class WwcwStateProperty(StrEnum):
    """Keys to read or write the WWCW (warm white/cold white) state."""

    BRIGHTNESS = "brightness"
    CURRENT_REGIME = "currRegime"
    ON = "on"
    PRESET_COLOR = "presetColor"
    PRESET_MOVIE = "presetMovie"
    TEMPERATURE = "temperature"


class LightRegime(StrEnum):
    """Possible regimes for the multi-color and WWCW outputs."""

    COLOR_SELECT = "ColorSelect"
    COLOR_WHEEL = "ColorWheel"
    MOVIE_SELECT = "MovieSelect"


# Deprecated: use LightRegime instead.
# Kept for backwards compatibility and will be removed in a future version.
MultiColorRegime = LightRegime


class _LightStateProperty(StrEnum):
    """Keys shared by all light states."""

    BRIGHTNESS = "brightness"
    CURRENT_REGIME = "currRegime"
    ON = "on"
    PRESET_COLOR = "presetColor"
    PRESET_MOVIE = "presetMovie"


class QbusMqttLightState(QbusMqttState):
    """Base MQTT representation of a Qbus LED light output."""

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
        return self.read_float_property(_LightStateProperty.BRIGHTNESS, None)

    def write_brightness(self, value: float) -> None:
        """Set the brightness of the Qbus output."""
        self.write_property(_LightStateProperty.BRIGHTNESS, value)

    def read_current_regime(self) -> LightRegime | None:
        """Read the current regime of the Qbus output."""
        value = self.read_str_property(_LightStateProperty.CURRENT_REGIME, None)
        return LightRegime(value) if value is not None else None

    def write_current_regime(self, value: LightRegime) -> None:
        """Set the current regime of the Qbus output."""
        self.write_property(_LightStateProperty.CURRENT_REGIME, value.value)

    def read_on(self) -> bool:
        """Read the on/off state of the Qbus output."""
        return self.read_bool_property(_LightStateProperty.ON, False)

    def write_on(self, value: bool) -> None:
        """Set the Qbus output on or off."""
        self.write_property(_LightStateProperty.ON, value)

    def read_preset_color(self) -> int | None:
        """Read the preset color of the Qbus output."""
        return self.read_int_property(_LightStateProperty.PRESET_COLOR, None)

    def write_preset_color(self, value: int) -> None:
        """Set the preset color of the Qbus output."""
        self.write_property(_LightStateProperty.PRESET_COLOR, value)

    def read_preset_movie(self) -> int | None:
        """Read the preset movie of the Qbus output."""
        return self.read_int_property(_LightStateProperty.PRESET_MOVIE, None)

    def write_preset_movie(self, value: int) -> None:
        """Set the preset movie of the Qbus output."""
        self.write_property(_LightStateProperty.PRESET_MOVIE, value)


class QbusMqttMultiColorState(QbusMqttLightState):
    """MQTT representation of a Qbus multi-color output."""

    def read_hue(self) -> float | None:
        """Read the hue of the Qbus output."""
        return self.read_float_property(MultiColorStateProperty.HUE, None)

    def write_hue(self, value: float) -> None:
        """Set the hue of the Qbus output."""
        self.write_property(MultiColorStateProperty.HUE, value)

    def read_saturation(self) -> float | None:
        """Read the saturation of the Qbus output."""
        return self.read_float_property(MultiColorStateProperty.SATURATION, None)

    def write_saturation(self, value: float) -> None:
        """Set the saturation of the Qbus output."""
        self.write_property(MultiColorStateProperty.SATURATION, value)


class QbusMqttWwcwState(QbusMqttLightState):
    """MQTT representation of a Qbus WWCW (warm white/cold white) output."""

    def read_temperature(self) -> float | None:
        """Read the color temperature of the Qbus output (0 to 100)."""
        return self.read_float_property(WwcwStateProperty.TEMPERATURE, None)

    def write_temperature(self, value: float) -> None:
        """Set the color temperature of the Qbus output (0 to 100)."""
        self.write_property(WwcwStateProperty.TEMPERATURE, value)
