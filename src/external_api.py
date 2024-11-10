import requests

from enviroment import (
    PrometheusValueName,
    PrometheusInstanceName,
    PrometheusJobName
)
from logger import logger
from promethus import push_to_promethus_gateway


def main():
    push_weather_data_to_prometheus()


def push_weather_data_to_prometheus() -> None:

    weather_data_json = get_weather_from_api()
    if weather_data_json:
        temperature_celsius = weather_data_json['main']['temp']
        humidity_celsius = weather_data_json['main']['humidity']
        cloud_coverage = weather_data_json['clouds']['all']
        push_to_promethus_gateway(temperature_celsius, PrometheusValueName.TEMPERATURE, PrometheusJobName.WEATHER_API, PrometheusInstanceName.OPENWEATHERMAP)
        push_to_promethus_gateway(humidity_celsius, PrometheusValueName.HUMIDITY, PrometheusJobName.WEATHER_API, PrometheusInstanceName.OPENWEATHERMAP)
        push_to_promethus_gateway(cloud_coverage, PrometheusValueName.CLOUD_COVERAGE, PrometheusJobName.WEATHER_API, PrometheusInstanceName.OPENWEATHERMAP)



def get_weather_from_api(units = "metric") -> any:

    api_key = get_key("api_key.key")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat=49.15&lon=9.21&appid={api_key}&units={units}"
    
    try:
        connection_api = requests.get(url)
        if connection_api.status_code == 200:
            logger.info(f"Connection to {url} was successfull with code {connection_api.status_code}")
            returned_data_json = connection_api.json()
            return returned_data_json
        else:
            logger.error(f"Connection to {url} failed with code {connection_api.status_code}.")
            return None
    except requests.exceptions.RequestException as exception:
        logger.critical(f"Connection to {url} could not be established. Error: {exception}")
        return None


def get_key(key_filename: str) -> str | None:
    try:
        with open(key_filename, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("api_key="):
                    return line.split("=", 1)[1].strip()
        logger.error(f"The api key file {key_filename} contains no api_key= line. No key was found")
        return None
    except FileNotFoundError:
        logger.error(f"The API Key file {key_filename} was not found.")
        return None
    except TypeError or AttributeError:
        logger.error(f"The API Key was not parsed correctly and was not passed a String")


if __name__ == "__main__":
    main()