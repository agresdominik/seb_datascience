from enum import Enum

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