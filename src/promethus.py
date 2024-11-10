from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from enviroment import (
    PUSHGATEWAY_URL,
    PrometheusValueName,
    PrometheusInstanceName,
    PrometheusJobName
)


def push_to_promethus_gateway(value: int, value_name: PrometheusValueName, job_name: PrometheusJobName, instance_name: PrometheusInstanceName, value_description = ""):
    """
    :param: value Is the Integer containig the value passed e.g. 23 for 23 Degrees Celsium Temperature
    :param: value_name Is the Name of the value, in our case this would be "Temperature", "Humidity" etc.
    :param: job_name  Is the grouping of data based on the souce the data comes from. E.g. "raspberry_pi_sensor_data" and "public_api_weather_data"
    :param: instance_name Is the name of the instance pushing this data. Could be useful if multiple raspberry pi push their own sensor data onto the pushgateway to seperate their values
    :param: value_description Is a optional description of the value passed along the value itself
    """

    #pushgateway_endpoint = PUSHGATEWAY_URL
    pushgateway_endpoint = ""

    # Create a registry for the metrics
    registry = CollectorRegistry()
    # Create a Gauge metric
    temperature_gauge = Gauge(value_name.value, value_description, labelnames=['instance'], registry=registry)
    # Set the temperature value
    temperature_gauge.labels(instance=instance_name.value).set(value)
    # Push the metrics to the Pushgateway
    push_to_gateway(pushgateway_endpoint, job=job_name.value, registry=registry)
