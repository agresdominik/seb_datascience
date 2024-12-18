import pandas as pd
from datetime import datetime

from env import ( 
    WINDOW_OPEN_TIMES
)


def main():

    data_list = read_collected_data()
    inside_temp_data = data_list[0]
    outside_temp_data = data_list[1]
    outside_humidity_data = data_list[2]
    inside_humidity_data = data_list[3]

    inside_temp_data = normalize_data(inside_temp_data, "temperature")
    outside_temp_data = normalize_data(outside_temp_data, "temperature")

    inside_humidity_data = normalize_data(inside_humidity_data, "humidity")
    outside_humidity_data = normalize_data(outside_humidity_data, "humidity")

    data = pd.merge_asof(inside_temp_data.sort_values('Time'), 
                     outside_temp_data.sort_values('Time'), 
                     on='Time', 
                     suffixes=('_inside', '_outside'))

    data = data.dropna()

    results = []

    for start in WINDOW_OPEN_TIMES:
        try:
            start_time = pd.to_datetime(start)
            temp_at_start = data.loc[data['Time'] == start_time, 'Temperature_inside'].values[0]
            outside_temp_at_start = data.loc[data['Time'] == start_time, 'Temperature_outside'].values[0]
            
            thirty_min_later = start_time + pd.Timedelta(minutes=30)
            temp_after_30_min = data.loc[data['Time'] == thirty_min_later, 'Temperature_inside'].values[0]
            outside_temp_after_30_min = data.loc[data['Time'] == thirty_min_later, 'Temperature_outside'].values[0]
            
            temp_drop = temp_at_start - temp_after_30_min
            temp_difference_at_start = temp_at_start - outside_temp_at_start
            temp_difference_at_end = temp_after_30_min - outside_temp_after_30_min
            average_temp_difference = (temp_difference_at_start + temp_difference_at_end) / 2
            cooling_rate = (temp_difference_at_start - temp_difference_at_end) / 30
            results.append({'start_time': start, 'drop_after_30_min': temp_drop, 'temp_difference_at_start': temp_difference_at_start, 'temp_difference_at_end': temp_difference_at_end, 'average_temp_difference': average_temp_difference, 'temp_at_start': temp_at_start, 'temp_after_30_min': temp_after_30_min, 'outside_temp_at_start': outside_temp_at_start, 'outside_temp_after_30_min': outside_temp_after_30_min, 'cooling_rate': cooling_rate})
        except Exception as e:
            data.to_csv("error_dump.csv", index=False)
            print(f"Error processing data for window open time: {start}, Exception: {e}")
    
    results_df = pd.DataFrame(results)
    results_df = results_df.round(3)

    write_data_to_csv(results_df, "temperature")


def write_data_to_csv(data_frame: pd.DataFrame, type_of_data: str) -> None:
    """
    This function writes the data to a csv file.
    """
    file_name = f"analasys_output_{type_of_data}.csv"
    data_frame.to_csv(file_name, index=False)


def read_collected_data() -> list[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    This function reads the collected data from the csv files and returns a list of two dataframes.
    The dataframes are labeled, their data is interpolated and resampled to 1 minute intervals.
    """
    
    inside_temp_data = pd.read_csv('/project/seb_datascience/src/data_processing/data/inside_temperature.csv', parse_dates=['Time'])
    inside_temp_data = inside_temp_data.iloc[1:].reset_index(drop=True)
    inside_temp_data.columns = ['Time', 'Temperature']
    inside_temp_data['Temperature'] = inside_temp_data['Temperature'].str.replace(' °C', '', regex=False).str.strip()
    inside_temp_data['Temperature'] = pd.to_numeric(inside_temp_data['Temperature'], errors='coerce')

    outside_temp_data = pd.read_csv('/project/seb_datascience/src/data_processing/data/outside_temperature.csv', parse_dates=['Time'])
    outside_temp_data = outside_temp_data.iloc[1:].reset_index(drop=True)
    outside_temp_data.columns = ['Time', 'Temperature']
    outside_temp_data['Temperature'] = outside_temp_data['Temperature'].str.replace(' °C', '', regex=False).str.strip()
    outside_temp_data['Temperature'] = pd.to_numeric(outside_temp_data['Temperature'], errors='coerce')

    inside_humidity_data = pd.read_csv('/project/seb_datascience/src/data_processing/data/inside_humidity.csv', parse_dates=['Time'])
    inside_humidity_data = inside_humidity_data.iloc[1:].reset_index(drop=True)
    inside_humidity_data['Humidity'] = inside_humidity_data['Humidity'].str.replace(' %', '', regex=False).str.strip()
    inside_humidity_data['Humidity'] = pd.to_numeric(inside_humidity_data['Humidity'], errors='coerce')

    outside_humidity_data = pd.read_csv('/project/seb_datascience/src/data_processing/data/outside_humidity.csv', parse_dates=['Time'])
    outside_humidity_data = outside_humidity_data.iloc[1:].reset_index(drop=True)
    outside_humidity_data['Humidity'] = outside_humidity_data['Humidity'].str.replace(' %', '', regex=False).str.strip()
    outside_humidity_data['Humidity'] = pd.to_numeric(outside_humidity_data['Humidity'], errors='coerce')

    #outside_temp_data = outside_temp_data.set_index('Time').resample('1T').interpolate('linear').reset_index()
    #inside_temp_data = inside_temp_data.set_index('Time').resample('1T').interpolate('linear').reset_index()
    #inside_humidity_data = inside_humidity_data.set_index('Time').resample('1T').interpolate('linear').reset_index()
    #outside_humidity_data = outside_humidity_data.set_index('Time').resample('1T').interpolate('linear').reset_index()

    data_list = [inside_temp_data, outside_temp_data, outside_humidity_data, inside_humidity_data]
    return data_list


def normalize_data(data_frame: pd.DataFrame, file_type: str) -> pd.DataFrame:
    """
    This function normalizes the data by removing outliers and interpolating the data to 1 minute intervals.
    """

    if file_type == "temperature":
        value = "Temperature"
        lower_percentile = 0.01
        upper_percentile = 99.99
    elif file_type == "humidity":
        value = "Humidity"
        lower_percentile = 0.1
        upper_percentile = 99.9
    else:
        raise ValueError("Invalid file type")

    lower_threshold = data_frame[value].quantile(lower_percentile / 100)
    upper_threshold = data_frame[value].quantile(upper_percentile / 100)

    df_filtered = data_frame[(data_frame[value] >= lower_threshold) & (data_frame[value] <= upper_threshold)]
    df_filtered = df_filtered.set_index('Time').resample('1T').interpolate('linear').reset_index()

    return df_filtered


if __name__ == "__main__":
    main()