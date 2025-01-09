import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import time


PROMETHEUS_URL = "http://192.168.0.222:9090/api/v1/query"

# create a model and define a goal temperature
data_results = pd.read_csv('/project/seb_datascience/src/web/training_data/analasys_output_temperature.csv', parse_dates=['start_time'])
collerate_data = data_results[['temp_difference_at_start', 'cooling_rate']]
X = collerate_data[['temp_difference_at_start']]
y = collerate_data['cooling_rate']
model = LinearRegression()
model.fit(X, y)

goal_temp = 22


def query_latest_prometheus_value(instance: str, metric_name: str):
    """
    Queries Prometheus for the latest value of a specific metric and instance.
    """
    query = f'last_over_time({metric_name}{{exported_instance="{instance}"}}[24h])'
    params = {"query": query}
    
    try:
        response = requests.get(PROMETHEUS_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
        if data["status"] == "success" and data["data"]["result"]:
            result = data["data"]["result"][0]
            value = result["value"]
            timestamp, metric_value = value
            return round(float(metric_value), 3)
        else:
            return "Error Querying Data"
    except Exception as e:
        return "No Connection to Proemtheus"


def get_window_opening_time(temp_inside: float, temp_outside: float) -> any:

    global goal_temp
    global model

    if goal_temp > temp_inside:
        return f"Temperature is below defined goal of {goal_temp}"

    temp_difference_actual = temp_inside - temp_outside
    goal_temperature_difference = goal_temp - temp_outside
    predicted_cooling_rate = model.predict([[temp_difference_actual]])[0]

    minute = 0

    while temp_difference_actual > goal_temperature_difference:
        temp_difference_actual -= predicted_cooling_rate
        minute += 1
        predicted_cooling_rate = model.predict([[temp_difference_actual]])[0]
        if minute >= 120:
            break

    return minute
