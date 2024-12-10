from time import sleep
from customExceptions import (
    DataMissingDHTError,
    DataMissingPublicAPIError,
    DataMissingMQError
)
from logger import logger
from temperature_humidity import (
    read_dht20
)
from external_api import (
    get_public_weather_data
)
from promethus import (
    raspberry_push_all_prometheus_data_in_one,
    push_all_prometheus_data_in_one
)


def main():

    public_weather_data_counter = 15

    while True:
        try:
            temperature_humidity = read_dht20()
            temperature = temperature_humidity[0]
            humidity = temperature_humidity[1]

            if public_weather_data_counter >= 15:

                try:
                    public_weather_data = get_public_weather_data()
                    outside_temperature = public_weather_data[0]
                    outside_humidity = public_weather_data[1]
                    outside_cloud_coverage = public_weather_data[2]
                    push_all_prometheus_data_in_one(temperature, humidity, outside_temperature, outside_humidity, outside_cloud_coverage)
                    public_weather_data_counter = 0
                except DataMissingPublicAPIError:
                    logger.error(f'API returned no value. Error: {DataMissingPublicAPIError}')
                    raspberry_push_all_prometheus_data_in_one(temperature, humidity)
            else:
                raspberry_push_all_prometheus_data_in_one(temperature, humidity)

        except DataMissingDHTError:
            logger.error(f'DHT Sensor not working. Error: {DataMissingDHTError}')
        except DataMissingMQError:
            logger.error(f'MQ Sensor not working. Error: {DataMissingMQError}')
        except:
            logger.error(f'Some other error plshelp')

        sleep(60)
        public_weather_data_counter += 1



if __name__ == "__main__":
    main()
