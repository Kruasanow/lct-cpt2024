import pandas as pd
import _pickle as cPickle
from datetime import datetime

from weather import get_weather


def predict_count_people(selected_day, latitude, longitude):
    hourly_dataframe, latitude, longitude, elevation = get_weather(92, 16, latitude, longitude)
    target_datetime = pd.to_datetime(selected_day.strftime('%Y-%m-%d'), utc=True)
    matching_rows = hourly_dataframe[hourly_dataframe['date'].dt.date == target_datetime.date()]

    with open('model.pkl', 'rb') as fid:
        model_load = cPickle.load(fid)

    def people_regression(df, model):
        df = df.drop(['date'], axis=1)
        return [int(i) for i in list(model.predict(df))]

    list_predict_people_on_day = people_regression(matching_rows, model_load)
    return sum(list_predict_people_on_day)


# print(predict_count_people(datetime(2024, 5, 3), 33.775219, 37.561395))