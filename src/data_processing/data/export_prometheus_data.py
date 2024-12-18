import requests
import csv
from datetime import datetime, timedelta

PROMETHEUS_URL = "http://192.168.0.222:9090/api/v1/query_range"
METRIC_NAMES = ["temperature", "humidity"]
INSTANCES = ["raspberry_pi", "openweathermap"]


def query_prometheus(instance: str, metric_name: str):

    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
    day += 1

    big_data = []
    start_time = datetime(2024, 11, 26, 0, 0)
    end_time = datetime(2024, 11, 27, 0, 0)
    total_end_time = datetime(year, month, day, 00, 00)

    while end_time <= total_end_time:
        params = {
            "query": f'{metric_name}{{exported_instance="{instance}"}}',
            "start": start_time.isoformat() + "Z",
            "end": end_time.isoformat() + "Z",
            "step": "1m"
        }
        try:
            response = requests.get(PROMETHEUS_URL, params=params)
            response.raise_for_status()  # Raise an error for HTTP issues
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error occurred: {e}")
        start_time = end_time
        end_time = end_time + timedelta(days=1)

        data = response.json()
        big_data.append(data)

    return big_data

def write_to_csv(instance: str, big_data: list, metric_name: str):

    if instance == "raspberry_pi":
        position = "inside"
    elif instance == "openweathermap":
        position = "outside"

    if metric_name == "temperature":
        metric_size = "°C"
        value_name = "Temperature"
    elif metric_name == "humidity":
        metric_size = "%"
        value_name = "Humidity"

    last_timestamp = ""

    file_name = f"{position}_{metric_name}.csv"
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", value_name])
        
        for data in big_data:
            for result in data.get("data", {}).get("result", []):
                for value in result["values"]:
                    timestamp, temp_value = value
                    time_str = datetime.utcfromtimestamp(float(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
                    if time_str == last_timestamp:
                        continue
                    last_timestamp = time_str
                    writer.writerow([time_str, f"{temp_value} {metric_size}"])
    
    print(f"Data written to {file_name}")


for metric_name in METRIC_NAMES:
    for instance in INSTANCES:
        try:
            print(f"Querying data for instance: {instance}")
            data = query_prometheus(instance, metric_name)
            write_to_csv(instance, data, metric_name)
        except Exception as e:
            print(f"An error occurred for instance {instance}: {e}")