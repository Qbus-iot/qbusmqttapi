"""Qbis discovery models."""

from __future__ import annotations

from enum import StrEnum

# Deprecated: use DiscoveryKey or DeviceKey instead.
# Kept for backwards compatibility and will be removed in a future version.
KEY_APP = "app"
KEY_DEVICES = "devices"

KEY_DEVICE_FUNCTIONBLOCKS = "functionBlocks"
KEY_DEVICE_ID = "id"
KEY_DEVICE_IP = "ip"
KEY_DEVICE_MAC = "mac"
KEY_DEVICE_NAME = "name"
KEY_DEVICE_SERIAL_NR = "serialNr"
KEY_DEVICE_TYPE = "type"
KEY_DEVICE_VERSION = "version"


class DiscoveryKey(StrEnum):
    """Top-level keys to read the discovery data."""

    APP = "app"
    DEVICES = "devices"


class DeviceKey(StrEnum):
    """Top-level keys to read the device data."""

    FUNCTIONBLOCKS = "functionBlocks"
    ID = "id"
    IP = "ip"
    MAC = "mac"
    NAME = "name"
    SERIAL_NR = "serialNr"
    TYPE = "type"
    VERSION = "version"


class OutputKey(StrEnum):
    """Top-level keys to read the output data."""

    ACTIONS = "actions"
    ID = "id"
    LOCATION = "location"
    LOCATION_ID = "locationId"
    NAME = "name"
    PROPERTIES = "properties"
    REF_ID = "refId"
    TYPE = "type"
    VARIANT = "variant"


class QbusMqttOutput:
    """MQTT representation of a Qbus output."""

    def __init__(self, data: dict, device: QbusMqttDevice) -> None:
        """Initialize based on a json loaded dictionary."""
        self._data = data
        self._device = device

    @property
    def id(self) -> str:
        """Return the id."""
        return self._data.get(OutputKey.ID) or ""

    @property
    def type(self) -> str:
        """Return the type."""
        return self._data.get(OutputKey.TYPE) or ""

    @property
    def name(self) -> str:
        """Return the name."""
        return self._data.get(OutputKey.NAME) or ""

    @property
    def ref_id(self) -> str:
        """Return the ref id."""
        return self._data.get(OutputKey.REF_ID) or ""

    @property
    def properties(self) -> dict:
        """Return the properties."""
        return self._data.get(OutputKey.PROPERTIES) or {}

    @property
    def actions(self) -> dict:
        """Return the actions."""
        return self._data.get(OutputKey.ACTIONS) or {}

    @property
    def location(self) -> str:
        """Return the location."""
        return self._data.get(OutputKey.LOCATION) or ""

    @property
    def location_id(self) -> int:
        """Return the location id."""
        return self._data.get(OutputKey.LOCATION_ID) or 0

    @property
    def variant(self) -> str | tuple | list:
        """Return the variant."""
        value = self._data.get(OutputKey.VARIANT) or ""

        if isinstance(value, list | tuple):
            value = [x for x in value if x is not None]

        return value

    @property
    def device(self) -> QbusMqttDevice:
        """Return the device."""
        return self._device


class QbusMqttDevice:
    """MQTT representation of a Qbus device."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self._data = data

    @property
    def id(self) -> str:
        """Return the id."""
        return self._data.get(DeviceKey.ID) or ""

    @property
    def ip(self) -> str:
        """Return the ip address."""
        return self._data.get(DeviceKey.IP) or ""

    @property
    def mac(self) -> str:
        """Return the ip address."""
        return self._data.get(DeviceKey.MAC) or ""

    @property
    def name(self) -> str:
        """Return the ip address."""
        return self._data.get(DeviceKey.NAME) or ""

    @property
    def serial_number(self) -> str:
        """Return the serial number."""
        return self._data.get(DeviceKey.SERIAL_NR) or ""

    @property
    def type(self) -> str:
        """Return the mac address."""
        return self._data.get(DeviceKey.TYPE) or ""

    @property
    def version(self) -> str:
        """Return the version."""
        return self._data.get(DeviceKey.VERSION) or ""

    @property
    def outputs(self) -> list[QbusMqttOutput]:
        """Return the outputs."""

        outputs: list[QbusMqttOutput] = []

        if self._data.get(DeviceKey.FUNCTIONBLOCKS):
            outputs = [QbusMqttOutput(x, self) for x in self._data[DeviceKey.FUNCTIONBLOCKS]]

        return outputs


class QbusDiscovery:
    """MQTT representation of a Qbus config."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self._devices = [QbusMqttDevice(x) for x in data.get(DiscoveryKey.DEVICES) or []]
        self._name: str = data.get(DiscoveryKey.APP) or ""

    def get_device_by_id(self, id: str) -> QbusMqttDevice | None:
        """Get the device by id."""
        return next((x for x in self.devices if x.id.casefold() == id.casefold()), None)

    def get_device_by_serial(self, serial: str) -> QbusMqttDevice | None:
        """Get the device by serial."""
        return next(
            (x for x in self.devices if x.serial_number.casefold() == serial.casefold()),
            None,
        )

    @property
    def devices(self) -> list[QbusMqttDevice]:
        """Return the devices."""
        return self._devices

    @property
    def name(self) -> str:
        """Return device name."""
        return self._name
