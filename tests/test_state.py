"""Tests for the state models."""

import pytest

from qbusmqttapi.state import (
    GaugeStateProperty,
    MultiColorRegime,
    QbusMqttAnalogState,
    QbusMqttDeviceState,
    QbusMqttGatewayState,
    QbusMqttGaugeState,
    QbusMqttHumidityState,
    QbusMqttMultiColorState,
    QbusMqttOnOffState,
    QbusMqttShutterState,
    QbusMqttState,
    QbusMqttStepperState,
    QbusMqttThermoState,
    QbusMqttVentilationState,
    QbusMqttWeatherState,
    StateAction,
    StateType,
)


def test_gateway_state() -> None:
    """Test the gateway state."""
    state = QbusMqttGatewayState({"id": "gw", "online": True, "reason": None})

    assert state.id == "gw"
    assert state.online is True
    assert state.reason is None


def test_gateway_state_empty() -> None:
    """Test the gateway state with missing values."""
    state = QbusMqttGatewayState({})

    assert state.id is None
    assert state.online is None
    assert state.reason is None


def test_device_state() -> None:
    """Test the device state with properties."""
    state = QbusMqttDeviceState(
        {"id": "UL1", "properties": {"connectable": False, "connected": True}}
    )

    assert state.id == "UL1"
    assert state.properties is not None
    assert state.properties.connectable is False
    assert state.properties.connected is True


def test_device_state_without_properties() -> None:
    """Test the device state without properties."""
    state = QbusMqttDeviceState({"id": "UL1"})

    assert state.id == "UL1"
    assert state.properties is None


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


def test_state_write_property() -> None:
    """Test writing properties creates and updates the properties."""
    state = QbusMqttState()

    state.write_property("value", 1)
    state.write_property("other", 2)
    state.write_property("value", 3)

    assert state.properties == {"value": 3, "other": 2}


def test_onoff_state() -> None:
    """Test the on/off state."""
    state = QbusMqttOnOffState(id="UL15", type=StateType.STATE)

    assert state.read_value() is False

    state.write_value(True)

    assert state.read_value() is True
    assert state.properties == {"value": True}


def test_analog_state() -> None:
    """Test the analog state."""
    state = QbusMqttAnalogState({"properties": {"value": 25.5}})

    assert state.read_percentage() == 25.5

    state.write_percentage(80)

    assert state.read_percentage() == 80
    assert QbusMqttAnalogState().read_percentage() is None


@pytest.mark.parametrize(("on", "action"), [(True, "on"), (False, "off")])
def test_analog_state_write_on_off(on: bool, action: str) -> None:
    """Test switching the analog output on or off sets the action."""
    state = QbusMqttAnalogState(id="UL16")

    state.write_on_off(on)

    assert state.action == action
    assert state.properties is None


def test_shutter_state() -> None:
    """Test the shutter state."""
    state = QbusMqttShutterState()

    assert state.read_state() is None
    assert state.read_position() is None
    assert state.read_slat_position() is None

    state.write_state("up")
    state.write_position(40)
    state.write_slat_position(60)

    assert state.read_state() == "up"
    assert state.read_position() == 40
    assert state.read_slat_position() == 60
    assert state.properties == {
        "state": "up",
        "shutterPosition": 40,
        "slatPosition": 60,
    }


def test_thermo_state() -> None:
    """Test the thermo state."""
    state = QbusMqttThermoState(
        {"properties": {"currTemp": 20.5, "setTemp": 21, "currRegime": "COMFORT"}}
    )

    assert state.read_current_temperature() == 20.5
    assert state.read_set_temperature() == 21
    assert state.read_regime() == "COMFORT"

    state.write_set_temperature(22.5)
    state.write_regime("NIGHT")

    assert state.read_set_temperature() == 22.5
    assert state.read_regime() == "NIGHT"


def test_thermo_state_defaults() -> None:
    """Test the thermo state without properties."""
    state = QbusMqttThermoState()

    assert state.read_current_temperature() is None
    assert state.read_set_temperature() is None
    assert state.read_regime() is None


def test_gauge_state() -> None:
    """Test the gauge state."""
    state = QbusMqttGaugeState({"properties": {"currentValue": 1.5}})

    assert state.read_value(GaugeStateProperty.CURRENT_VALUE) == 1.5
    assert state.read_value(GaugeStateProperty.CONSUMPTION_VALUE) == 0


def test_ventilation_state() -> None:
    """Test the ventilation state."""
    state = QbusMqttVentilationState(
        {"properties": {"co2": 650.5, "refresh": 2, "currRegime": "AUTO"}}
    )

    assert state.read_co2() == 650.5
    assert state.read_refresh() == 2
    assert state.read_regime() == "AUTO"

    state.write_regime("MANUAL")

    assert state.read_regime() == "MANUAL"


def test_ventilation_state_defaults() -> None:
    """Test the ventilation state without properties."""
    state = QbusMqttVentilationState()

    assert state.read_co2() == 0
    assert state.read_refresh() == 0
    assert state.read_regime() is None


def test_humidity_state() -> None:
    """Test the humidity state."""
    state = QbusMqttHumidityState({"properties": {"value": 55.5, "currRegime": "AUTO"}})

    assert state.read_value() == 55.5
    assert state.read_regime() == "AUTO"

    state.write_regime("MANUAL")

    assert state.read_regime() == "MANUAL"


def test_humidity_state_defaults() -> None:
    """Test the humidity state without properties."""
    state = QbusMqttHumidityState()

    assert state.read_value() == 0
    assert state.read_regime() is None


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


def test_stepper_state() -> None:
    """Test the stepper state."""
    state = QbusMqttStepperState()

    assert state.read_value() is None

    state.write_value(3)

    assert state.read_value() == 3
    assert state.properties == {"value": 3}


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
