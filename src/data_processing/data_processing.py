import pandas as pd
from datetime import datetime


def main():

    data_list = read_collected_data()
    inside_temp_data = data_list[0]
    outside_temp_data = data_list[1]

    inside_temp_data = normalize_data(inside_temp_data, "temperature", "inside")
    outside_temp_data = normalize_data(outside_temp_data, "temperature", "outside")

    data = pd.merge_asof(inside_temp_data.sort_values('Time'), 
                     outside_temp_data.sort_values('Time'), 
                     on='Time', 
                     suffixes=('_inside', '_outside'))

    data = data.dropna()

    print(data.head())

    """ 
    # window open times in CET time, because Prometheus export is in utc see set below
    window_open_times = [
        ('2024-12-01 23:15:00', '2024-12-01 23:45:00'),
        ('2024-12-02 12:05:00', '2024-12-02 12:35:00'),
        ('2024-12-03 19:10:00', '2024-12-03 19:40:00'),
        ('2024-12-04 08:27:00', '2024-12-04 08:57:00'),
        ('2024-12-05 22:20:00', '2024-12-05 22:50:00'),
        ('2024-12-06 07:59:00', '2024-12-06 08:29:00'),
        ('2024-12-06 14:51:00', '2024-12-06 15:21:00'),
        ('2024-12-07 06:35:00', '2024-12-07 07:05:00'),
        ('2024-12-08 09:06:30', '2024-12-08 09:36:30'),
        ('2024-12-08 18:25:30', '2024-12-08 18:55:30'),
        ('2024-12-09 23:00:00', '2024-12-09 23:30:00'),
        ('2024-12-10 07:32:00', '2024-12-10 08:02:00'),
        ('2024-12-10 18:08:00', '2024-12-10 18:38:00')
    ]
    """

    window_open_times = [
        ('2024-12-01 22:00:00'),
        ('2024-12-02 11:05:00'),
        ('2024-12-03 18:10:00'),
        ('2024-12-04 07:27:00'),
        ('2024-12-05 21:20:00'),
        ('2024-12-06 06:59:00'),
        ('2024-12-06 13:51:00'),
        ('2024-12-07 05:35:00'),
        ('2024-12-08 08:06:00'),
        ('2024-12-08 17:25:00'),
        ('2024-12-09 22:00:00'),
        ('2024-12-10 06:32:00'),
        ('2024-12-10 17:08:00'),
        ('2024-12-10 20:15:00'),
        ('2024-12-10 22:27:00'),
        ('2024-12-11 07:30:00'),
        ('2024-12-11 09:15:00'),
        ('2024-12-11 12:13:00'),
        ('2024-12-14 12:45:00'),
        ('2024-12-15 14:02:00')
    ]

    results = []

    for start in window_open_times:
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
    print(results_df.to_string())

    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    file_name = f"analasys_output_{timestamp_str}.csv"
    results_df.to_csv(file_name, index=False)



def read_collected_data() -> list[pd.DataFrame, pd.DataFrame]:
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

    outside_temp_data = outside_temp_data.set_index('Time').resample('1T').interpolate('linear').reset_index()
    inside_temp_data = inside_temp_data.set_index('Time').resample('1T').interpolate('linear').reset_index()

    data_list = [inside_temp_data, outside_temp_data]
    return data_list


def normalize_data(data_frame: pd.DataFrame, file_type: str, data_source: str) -> pd.DataFrame:
    """
    This function normalizes the data by removing outliers and interpolating the data to 1 minute intervals.
    """

    if file_type == "temperature":
        value = "Temperature"
    elif file_type == "humidity":
        value = "Humidity"
    else:
        raise ValueError("Invalid file type")

    lower_threshold = data_frame[value].quantile(0.01 / 100)
    upper_threshold = data_frame[value].quantile(99.99 / 100)


    df_filtered = data_frame[(data_frame[value] >= lower_threshold) & (data_frame[value] <= upper_threshold)]
    #removed_data = data_frame[(data_frame[value] < lower_threshold) | (data_frame[value] > upper_threshold)]

    df_filtered = df_filtered.set_index('Time').resample('1T').interpolate('linear').reset_index()

    #print(df_filtered.to_string())
    #print("Removed data:" + removed_data.to_string())
    return df_filtered


if __name__ == "__main__":
    main()