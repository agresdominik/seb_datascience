import time
import adafruit_dht

from enviroment import (
    DHT_22_PIN,
    PrometheusValueName,
    PrometheusInstanceName,
    PrometheusJobName
)
from promethus import (
    push_to_promethus_gateway
)
from logger import logger

def readout_dht22() -> None:

    logger.debug("Starting dht function")
    dht_sensor = adafruit_dht.DHT22(DHT_22_PIN)

    try:
        logger.debug("Reading DHT")
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
    except:
        dht_sensor.exit()
        logger.error("No data in DHT")
        return None

    try:
        logger.debug("Sending data to pushgateway")
        push_to_promethus_gateway(temperature, PrometheusValueName.TEMPERATURE, PrometheusJobName.RASPBERRY_PI, PrometheusInstanceName.RASPBERRY_PI_1)
        push_to_promethus_gateway(humidity, PrometheusValueName.HUMIDITY, PrometheusJobName.RASPBERRY_PI, PrometheusInstanceName.RASPBERRY_PI_1)
    except:
        logger.error("Error in sending data")
        return None

