"""Parser for Govee BLE advertisements.

"""
from __future__ import annotations

import logging
import struct

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorLibrary
from sensor_state_data import (
    DeviceClass,
    DeviceKey,
    SensorDescription,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
    Units,
)

_LOGGER = logging.getLogger(__name__)
__version__ = "0.20.0"

__all__ = [
    "GoveeBluetoothDeviceData",
    "SensorDescription",
    "SensorDeviceInfo",
    "DeviceClass",
    "DeviceKey",
    "SensorUpdate",
    "SensorDeviceInfo",
    "SensorValue",
    "Units",
]

class GoveeBluetoothDeviceData(BluetoothData):
    """Data for Govee BLE sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing Renpho BLE service_info data: %s", service_info)
        manufacturer_data = service_info.manufacturer_data
        _LOGGER.debug("Parsing Renpho BLE manufacturer_data data: %s", manufacturer_data)
        address = service_info.address
        _LOGGER.debug("Renpho Address: " + str(address))
        
        
        for mfr_id, mfr_data in manufacturer_data.items():
            _LOGGER.debug("mfr_id: " + str(mfr_id))
            _LOGGER.debug("mfr_data: " + str(mfr_data))
            if mfr_id == 65535:
                _LOGGER.debug("Parsing Renpho BLE mfr data: %s", str(mfr_data))
                subbytes=mfr_data[17:19]
                weight = int.from_bytes(subbytes, "little") / 100
                _LOGGER.debug("weight: " + str(weight))
                if weight > 0:
                    self.set_device_manufacturer("Renpho")
                    self.set_device_name("Scale " + str(address))
                    self.set_device_type("Renpho BLE Scale")
                    self.set_precision(2)
                    self.update_predefined_sensor(SensorLibrary.MASS__MASS_KILOGRAMS, weight)