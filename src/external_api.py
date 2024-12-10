import requests
import os
from enviroment import (
    KEY_FILE_PATH
)
from customExceptions import DataMissingPublicAPIError
from logger import logger


def get_public_weather_data() -> list:
    weather_data_json = _get_weather_from_api()
    if weather_data_json:
        try:
            temperature_celsius = weather_data_json['main']['temp']
            humidity_celsius = weather_data_json['main']['humidity']
            cloud_coverage = weather_data_json['clouds']['all']
            return [temperature_celsius, humidity_celsius, cloud_coverage]
        except:
            logger.error("An error raised while parsing API Weather data and sending it to Prometheus")
            raise DataMissingPublicAPIError
    else:
        logger.error("Returned weather data was null.")
        raise DataMissingPublicAPIError


def _get_weather_from_api(units = "metric") -> any:

    api_key = _get_key()

    url = f"https://api.openweathermap.org/data/2.5/weather?lat=49.15&lon=9.21&appid={api_key}&units={units}"
    
    try:
        connection_api = requests.get(url)
        if connection_api.status_code == 200:
            logger.debug(f"Connection to {url} was successfull with code {connection_api.status_code}")
            returned_data_json = connection_api.json()
            return returned_data_json
        else:
            logger.error(f"Connection to {url} failed with code {connection_api.status_code}.")
            return None
    except requests.exceptions.RequestException as exception:
        logger.critical(f"Connection to {url} could not be established. Error: {exception}")
        return None


def _get_key() -> str | None:
    try:
        with open(KEY_FILE_PATH, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("api_key="):
                    return line.split("=", 1)[1].strip()
        logger.error(f"The api key file {KEY_FILE_PATH} contains no api_key= line. No key was found")
        return None
    except FileNotFoundError:
        logger.error(f"The API Key file {KEY_FILE_PATH} was not found.")
        return None
    except TypeError or AttributeError:
        logger.error(f"The API Key was not parsed correctly and was not passed a String")
