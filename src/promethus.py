from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from enviroment import (
    PUSHGATEWAY_URL
)


def push_to_promethus_gateway(value: any, value_name: str):

    # Pushgateway details
    #pushgateway_endpoint = PUSHGATEWAY_URL
    pushgateway_endpoint = ""
    job_name = "raspberry_pi_sensor_data"

    # Create a registry for the metrics
    registry = CollectorRegistry()

    # Create a Gauge metric
    temperature_gauge = Gauge(value_name, '', labelnames=['instance'], registry=registry)

    # Set the temperature value
    temperature_gauge.labels(instance="raspberryPi").set(value)

    # Push the metrics to the Pushgateway
    push_to_gateway(pushgateway_endpoint, job=job_name, registry=registry)
