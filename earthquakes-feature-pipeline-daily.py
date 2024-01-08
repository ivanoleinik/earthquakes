import os
import numpy as np
import pandas as pd
import hopsworks
import requests
import io
from datetime import date, timedelta


def get_earthquakes(date=date.today()):
    params = {
        'format': 'csv',
        'starttime': date - timedelta(days=1),
        'endtime': date
    }

    r = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query', params=params)
    earthquakes_df = pd.read_csv(io.StringIO(r.text))

    return earthquakes_df


def filter_earthquakes(df):
    df.dropna(inplace=True)
    df = df[['id', 'time', 'latitude', 'longitude', 'depth', 'depthError', 'rms', 'status', 'type', 'mag']]
    df = df[df.type == 'earthquake']
    df['reviewed'] = (df['status'] == 'reviewed').astype(float)
    df.drop(columns=['type', 'status'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={'depthError': 'deptherror'}, inplace=True)
    return df


def add_earthquakes():
    project = hopsworks.login()
    fs = project.get_feature_store()

    earthquakes_df = filter_earthquakes(get_earthquakes())

    earthquakes_fg = fs.get_feature_group(name="earthquakes", version=1)
    earthquakes_fg.insert(earthquakes_df)


if __name__ == "__main__":
    add_earthquakes()
