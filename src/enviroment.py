from enum import Enum
import os

KEY_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"api_key.key")

I2C_BUS: int     = 0x01  # default use I2C1 bus
I2C_DHT_ADDRESS: int = 0x38  # I2C Address for DHT20
PUSHGATEWAY_URL="http://192.168.0.222:9091"

class PrometheusValueName(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    CLOUD_COVERAGE = "cloud_coverage"
    AIR_QUALITY = "air_quality"
    

class PrometheusJobName(Enum):
    RASPBERRY_PI = "raspberry_pi_sensor_data"
    WEATHER_API = "public_api_weather_data"
    

class PrometheusInstanceName(Enum):
    RASPBERRY_PI_1 = "raspberry_pi"
    OPENWEATHERMAP = "openweathermap"