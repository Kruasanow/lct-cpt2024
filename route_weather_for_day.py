from weather import *
import pandas as pd
from datetime import datetime


def get_weather_for_selected_day(selected_day, latitude, longitude):
    hourly_dataframe, latitude, longitude, elevation = get_weather(92, 16, latitude, longitude)
    target_datetime = pd.to_datetime(selected_day.strftime('%Y-%m-%d 12:00:00'), utc=True)
    matching_row = hourly_dataframe[hourly_dataframe['date'] == target_datetime]
    weather_for_selected_day = {}
    if not matching_row.empty:
        weather_for_selected_day['temperature'] = str(matching_row['temperature_2m'].values[0])
        weather_for_selected_day['wind_speed'] = str(matching_row['wind_speed_10m'].values[0])
        if matching_row['cloud_cover'].values[0] > 20:
            weather_for_selected_day['status'] = 'cloudy'
        else:
            weather_for_selected_day['status'] = 'clear'
        if matching_row['rain'].values[0] > 0:
            weather_for_selected_day['status'] = 'rain'
        if matching_row['rain'].values[0] > 1.0:
            weather_for_selected_day['status'] = 'thunderstorm'
    else:
        weather_for_selected_day['message'] = 'There is no weather for this day'
    return weather_for_selected_day


# Входные данные
"""
    дата, широта, долгота
"""
# print(get_weather_for_selected_day(datetime(2024, 5, 3), 55.775219, 37.561395))
# Пример выхода
"""
    {'message': 'There is no weather for this day'}

или

    {'temperature': 9.496, 'wind_speed': 2.4515302, 'status': 'clear'}
"""