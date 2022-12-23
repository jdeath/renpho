"""
Detection callback w/ scanner
--------------

Example showing what is returned using the callback upon detection functionality

Updated on 2020-10-11 by bernstern <bernie@allthenticate.net>
    
"""

import asyncio
import logging
import sys
import binascii

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

logger = logging.getLogger(__name__)


def simple_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    
    if device.address == "ED:67:39:70:01:65":
        
        advertisementBytes = device.details['props']['ManufacturerData'][65535]
        subbytes=advertisementBytes[17:19]
        int_val = int.from_bytes(subbytes, "little") / 100
        print("wieght: " + str(int_val))
       
     
async def main(service_uuids):
    scanner = BleakScanner(simple_callback, service_uuids)

    while True:
        print("(re)starting scanner")
        await scanner.start()
        await asyncio.sleep(5.0)
        await scanner.stop()


if __name__ == "__main__":
    
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )
    service_uuids = sys.argv[1:]
    asyncio.run(main(service_uuids))
