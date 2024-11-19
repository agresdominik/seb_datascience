import time
import smbus2 as smbus

                
class DHT20_SENSOR(object):

  def __init__(self, bus: int, address: int) -> None:
    self.i2cbus = smbus.SMBus(bus)
    self._addr = address


  def begin(self) -> bool:
    # after power-on, wait no less than 100ms
    time.sleep(0.5)

    # check and return initialization status, see datasheet
    data = self.__read_reg(0x71,1)
    if (data[0] & 0x18) != 0x18:
      return False
    else:
      return True


  def get_temperature_and_humidity(self) -> tuple[float, float, bool]:
    """Get both temperature and humidity in a single read.

    [!] Do not call this function more often than 2 seconds as recommended by the
    datasheet to prevent rise in sensor temperature that will affect its accuracy. 

    Returns:
      The temperature (±0.5℃), humidity (±3%) and 
      CRC result (True if error else False) as a tuple.
    """

    # trigger measurement
    self.__write_reg(0xac,[0x33,0x00])

    # wait 80 ms and keep waiting until the measurement is completed
    while True:
      time.sleep(0.08)
      data = self.__read_reg(0x71,1)
      if (data[0] & 0x80) == 0:
        break

    # read sensor data
    data = self.__read_reg(0x71,7)

    # extract and convert temperature and humidity from data
    temperature_rawData: int = ((data[3]&0xf) << 16) + (data[4] << 8) + data[5]
    humidity_rawData: int = ((data[3]&0xf0) >> 4) + (data[1] << 12) + (data[2] << 4)
    temperature: float = float(temperature_rawData) / 5242.88 - 50
    humidity: float = float(humidity_rawData) / 0x100000 * 100

    # check CRC
    crc_error: bool = self.__calc_CRC8(data) != data[6]

    # return results
    return (temperature, humidity, crc_error)


  def __calc_CRC8(self, data: list[int]) -> int:
    """Calculate CRC-8.

    Args:
      data: Data from sensor which its CRC-8 is to be calculated.

    Returns:
      Calculated CRC-8
    """

    crc: int = 0xFF

    for i in data[:-1]:
      crc ^= i
      for _ in range(8):
        if crc & 0x80:
          crc = (crc << 1)^0x31
        else:
          crc = crc << 1
    
    return (crc & 0xFF)

  
  def __write_reg(self, reg: int, data: list[int]) -> None:
    time.sleep(0.01)
    self.i2cbus.write_i2c_block_data(self._addr,reg,data)
  
  
  def __read_reg(self, reg: int, len: int) -> list[int]:
    time.sleep(0.01)
    rslt: list[int] = self.i2cbus.read_i2c_block_data(self._addr,reg,len)
    return rslt
