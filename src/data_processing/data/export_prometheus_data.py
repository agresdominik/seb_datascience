import requests
import csv
from datetime import datetime, timedelta

# Prometheus server URL
PROMETHEUS_URL = "http://192.168.0.222:9090/api/v1/query_range"

# Define the metric and the instances
METRIC_NAME = "temperature"
INSTANCES = ["raspberry_pi", "openweathermap"]


def query_prometheus(instance):
    
    big_data = []
    start_time = datetime(2024, 11, 26, 0, 0)
    end_time = datetime(2024, 11, 27, 0, 0)
    total_end_time = datetime(2024, 12, 11, 00, 00)

    while end_time <= total_end_time:
        params = {
            "query": f'{METRIC_NAME}{{exported_instance="{instance}"}}',
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
        start_time = end_time + timedelta(seconds=1)
        end_time = end_time + timedelta(days=1)

        data = response.json()
        big_data.append(data)

    #data = response.json()
    return big_data

def write_to_csv(instance, big_data):
    """Write the Prometheus data to a CSV file."""
    file_name = f"{instance}_temperature.csv"
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Value"])
        
        for data in big_data:
            # Extract metric values
            for result in data.get("data", {}).get("result", []):
                for value in result["values"]:
                    timestamp, temp_value = value
                    time_str = datetime.utcfromtimestamp(float(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([time_str, f"{temp_value} °C"])
    
    print(f"Data written to {file_name}")

# Main process
for instance in INSTANCES:
    try:
        print(f"Querying data for instance: {instance}")
        data = query_prometheus(instance)
        write_to_csv(instance, data)
    except Exception as e:
        print(f"An error occurred for instance {instance}: {e}")