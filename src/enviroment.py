import board
from enum import Enum

DHT_22_PIN = board.D4
AIR_QUALITY_SENSOR_PIN = ""
PHOTOSENSOR_PIN = ""

PUSHGATEWAY_URL="http://localhost:9091"

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