import time
import adafruit_dht

from enviroment import (
    DHT_22_PIN
)
from promethus import (
    push_to_promethus_gateway
)
from logger import logger

def readout_dht22():

    logger.info("Starting dht function")
    dht_sensor = adafruit_dht.DHT22(DHT_22_PIN)

    try:
        logger.info("Reading DHT")
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity

    except:
        dht_sensor.exit()
        logger.error("No data in DHT")
        return None


    try:
        logger.info("Sending data to pushgateway")
        push_to_promethus_gateway(temperature, "temperature_indoors")
        push_to_promethus_gateway(humidity, "humidity_indoors")

    except:
        logger.error("Error in sending data")
        return None

    time.sleep(2.0)
