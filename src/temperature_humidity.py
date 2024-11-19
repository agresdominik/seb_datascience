from time import strftime

from sensors.dht20 import (
    DHT20_SENSOR
)


I2C_BUS: int     = 0x01  # default use I2C1 bus
I2C_ADDRESS: int = 0x38  # I2C Address for DHT20

dht20 = DHT20_SENSOR(I2C_BUS, I2C_ADDRESS)

def _initialise_dht20() -> bool:
   return dht20.begin()


def read_dht20() -> list:
    if _initialise_dht20():
        # Read ambient temperature and relative humidity and print them to terminal
        print(strftime("%Y-%m-%d %H:%M:%S %Z"))
        T_celcius, humidity, crc_error = dht20.get_temperature_and_humidity()
        if crc_error:
            print("CRC               : Error\n")
        else:
            print(f"Temperature       : {T_celcius}°C")
            print(f"Relative Humidity : {humidity}%")
            print("CRC                : OK\n")
            return [T_celcius, humidity]
    else:
        return [0, 0] 