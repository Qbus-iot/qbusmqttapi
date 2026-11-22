"""Qbus state models."""

from .analog import AnalogStateProperty, QbusMqttAnalogState
from .base import QbusMqttState, StateAction, StateKey, StateType
from .device import (
    DeviceStateKey,
    DeviceStateProperty,
    QbusMqttDeviceState,
    QbusMqttDeviceStateProperties,
)
from .gateway import GatewayStateKey, QbusMqttGatewayState
from .gauge import GaugeStateProperty, QbusMqttGaugeState
from .humidity import HumidityStateProperty, QbusMqttHumidityState
from .light import (
    LightRegime,
    MultiColorRegime,
    MultiColorStateProperty,
    QbusMqttLightState,
    QbusMqttMultiColorState,
    QbusMqttWwcwState,
    WwcwStateProperty,
)
from .onoff import OnOffStateProperty, QbusMqttOnOffState
from .shutter import QbusMqttShutterState, ShutterStateProperty
from .stepper import QbusMqttStepperState, StepperStateProperty
from .thermo import QbusMqttThermoState, ThermoStateProperty
from .ventilation import QbusMqttVentilationState, VentilationStateProperty
from .weather import QbusMqttWeatherState, WeatherStationStateProperty

# Deprecated: use DeviceStateKey, DeviceStateProperty or GatewayStateKey instead.
# Kept for backwards compatibility and will be removed in a future version.
KEY_DEVICE_CONNECTABLE = "connectable"
KEY_DEVICE_CONNECTED = "connected"
KEY_DEVICE_ID = "id"
KEY_DEVICE_STATE_PROPERTIES = "properties"

KEY_GATEWAY_ID = "id"
KEY_GATEWAY_ONLINE = "online"
KEY_GATEWAY_REASON = "reason"

__all__ = [
    "KEY_DEVICE_CONNECTABLE",
    "KEY_DEVICE_CONNECTED",
    "KEY_DEVICE_ID",
    "KEY_DEVICE_STATE_PROPERTIES",
    "KEY_GATEWAY_ID",
    "KEY_GATEWAY_ONLINE",
    "KEY_GATEWAY_REASON",
    "AnalogStateProperty",
    "DeviceStateKey",
    "DeviceStateProperty",
    "GatewayStateKey",
    "GaugeStateProperty",
    "HumidityStateProperty",
    "LightRegime",
    "MultiColorRegime",
    "MultiColorStateProperty",
    "OnOffStateProperty",
    "QbusMqttAnalogState",
    "QbusMqttDeviceState",
    "QbusMqttDeviceStateProperties",
    "QbusMqttGatewayState",
    "QbusMqttGaugeState",
    "QbusMqttHumidityState",
    "QbusMqttLightState",
    "QbusMqttMultiColorState",
    "QbusMqttOnOffState",
    "QbusMqttShutterState",
    "QbusMqttState",
    "QbusMqttStepperState",
    "QbusMqttThermoState",
    "QbusMqttVentilationState",
    "QbusMqttWeatherState",
    "QbusMqttWwcwState",
    "ShutterStateProperty",
    "StateAction",
    "StateKey",
    "StateType",
    "StepperStateProperty",
    "ThermoStateProperty",
    "VentilationStateProperty",
    "WeatherStationStateProperty",
    "WwcwStateProperty",
]
