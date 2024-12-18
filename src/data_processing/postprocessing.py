import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def main():
    data_results = pd.read_csv('/project/seb_datascience/src/data_processing/analasys_output_2024-12-17_10-42-44.csv', parse_dates=['start_time'])

    collerate_data = data_results[['temp_difference_at_start', 'cooling_rate']]
    print(collerate_data.corr())

    X = collerate_data[['temp_difference_at_start']]
    y = collerate_data['cooling_rate']
    model = LinearRegression()
    model.fit(X, y)

    print(f"Model coefficient: {model.coef_[0]}")
    print(f"Model intercept: {model.intercept_}")

    temp_difference_at_start_predict = 25

    predicted_cooling_rate = model.predict([[temp_difference_at_start_predict]])
    print(f"Predicted cooling rate per minute: {predicted_cooling_rate}")

    minutes = 30
    temp_time = predicted_cooling_rate * minutes

    print(f"How many degrees will cool after {minutes} minutes at {temp_difference_at_start_predict} degrees difference: {temp_time}")



if __name__ == "__main__":
    main()