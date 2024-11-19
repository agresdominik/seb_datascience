import requests

from enviroment import (
    PUSHGATEWAY_URL,
    PrometheusValueName,
    PrometheusInstanceName,
    PrometheusJobName
)


def raspberry_push_all_prometheus_data_in_one(value_temperature: int, value_humidity: int) -> None:
    instance = PrometheusInstanceName.RASPBERRY_PI_1
    job = PrometheusJobName.RASPBERRY_PI
    temperature_value_name = PrometheusValueName.TEMPERATURE
    humidity_value_name = PrometheusValueName.HUMIDITY

    metric_tmp = f"{temperature_value_name.value}{{instance=\"{instance.value}\",job=\"{job.value}\"}} {value_temperature}\n"
    metric_hmd = f"{humidity_value_name.value}{{instance=\"{instance.value}\",job=\"{job.value}\"}} {value_humidity}\n"

    metrics_payload = metric_hmd + metric_tmp
    pushgateway_endpoint = f"{PUSHGATEWAY_URL}/metrics/job/{job.value}"

    _push_to_gateway(pushgateway_endpoint, metrics_payload)


def push_all_prometheus_data_in_one(value_temperature: int, value_humidity: int, value_temperature_outside: int, value_humidity_outside: int, value_cloud_coverage_outside: int) -> None:
    raspi_instance = PrometheusInstanceName.RASPBERRY_PI_1
    openweather_instance = PrometheusInstanceName.OPENWEATHERMAP
    raspi_job = PrometheusJobName.RASPBERRY_PI
    temperature_value_name = PrometheusValueName.TEMPERATURE
    humidity_value_name = PrometheusValueName.HUMIDITY
    cloud_coverage_value_name = PrometheusValueName.CLOUD_COVERAGE

    metric_tmp = f"{temperature_value_name.value}{{instance=\"{raspi_instance.value}\",job=\"{raspi_job.value}\"}} {value_temperature}\n"
    metric_hmd = f"{humidity_value_name.value}{{instance=\"{raspi_instance.value}\",job=\"{raspi_job.value}\"}} {value_humidity}\n"
    metric_tmp_outside = f"{temperature_value_name.value}{{instance=\"{openweather_instance.value}\",job=\"{raspi_job.value}\"}} {value_temperature_outside}\n"
    metric_hmd_outside = f"{humidity_value_name.value}{{instance=\"{openweather_instance.value}\",job=\"{raspi_job.value}\"}} {value_humidity_outside}\n"
    metric_cldco_outside = f"{cloud_coverage_value_name.value}{{instance=\"{openweather_instance.value}\",job=\"{raspi_job.value}\"}} {value_cloud_coverage_outside}\n"
   
    metrics_payload = metric_tmp + metric_hmd + metric_tmp_outside + metric_hmd_outside + metric_cldco_outside
    pushgateway_endpoint = f"{PUSHGATEWAY_URL}/metrics/job/{raspi_job.value}"
    _push_to_gateway(pushgateway_endpoint, metrics_payload)


def push_to_promethus_gateway_single_value(value: int, value_name: PrometheusValueName, job_name: PrometheusJobName, instance_name: PrometheusInstanceName, value_description = "") -> None:
    """
    :param: value Is the Integer containig the value passed e.g. 23 for 23 Degrees Celsium Temperature
    :param: value_name Is the Name of the value, in our case this would be "Temperature", "Humidity" etc.
    :param: job_name  Is the grouping of data based on the souce the data comes from. E.g. "raspberry_pi_sensor_data" and "public_api_weather_data"
    :param: instance_name Is the name of the instance pushing this data. Could be useful if multiple raspberry pi push their own sensor data onto the pushgateway to seperate their values
    :param: value_description Is a optional description of the value passed along the value itself
    """

    metric = f"{value_name.value}{{instance=\"{instance_name.value}\",job=\"{job_name.value}\"}} {value}\n"
    pushgateway_endpoint = f"{PUSHGATEWAY_URL}/metrics/job/{job_name.value}"
    _push_to_gateway(pushgateway_endpoint, metric)


def _push_to_gateway(pushgateway_endpoint: str, metrics_payload: any) -> int | None:
    try:
        response = requests.post(pushgateway_endpoint, data=metrics_payload)
        return response.status_code
    except:
        # No connection could be made at all
        return None
