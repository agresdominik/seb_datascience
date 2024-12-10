from time import strftime

from customExceptions import DataMissingDHTError
from sensors.dht20 import (
    DHT20_SENSOR
)
from enviroment import (
    I2C_BUS,
    I2C_DHT_ADDRESS
)

dht20 = DHT20_SENSOR(I2C_BUS, I2C_DHT_ADDRESS)

def _initialise_dht20() -> bool:
   return dht20.begin()


def read_dht20() -> list:
    if _initialise_dht20():
        # Read ambient temperature and relative humidity and print them to terminal
        T_celcius, humidity, crc_error = dht20.get_temperature_and_humidity()
        if crc_error:
            raise DataMissingDHTError("Parity Bit calculated wrong.")
        else:
            return [T_celcius, humidity]
    else:
        raise DataMissingDHTError("DHT20 Sensor could not be initialised.")