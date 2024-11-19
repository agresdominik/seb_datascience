from time import sleep

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
    public_weather_data_counter = 0
    while True:
        temperature_humidity = read_dht20()
        temperature = temperature_humidity[0]
        humidity = temperature_humidity[1]

        public_weather_data_counter += 1

        if public_weather_data_counter == 15:
            public_weather_data = get_public_weather_data()
            outside_temperature = public_weather_data[0]
            outside_humidity = public_weather_data[1]
            outside_cloud_coverage = public_weather_data[2]

            push_all_prometheus_data_in_one(temperature, humidity, outside_temperature, outside_humidity, outside_cloud_coverage)
            public_weather_data_counter = 0
        else:
            raspberry_push_all_prometheus_data_in_one(temperature, humidity)

        sleep(60)


if __name__ == "__main__":
    main()
