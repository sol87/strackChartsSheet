# -*- coding: UTF-8 -*-

import os
import datetime as dt
import pandas as pd
import numpy as np


class TimelogModel(object):
    COLOR_MAP = {
        'work': '#67C23A'
    }

    def __init__(self, csv_path='../src_data/time_log.csv'):
        self.__csv_path = csv_path
        self.__df = self.get_timelog_data_frame()

    @property
    def df(self):
        return self.__df

    @property
    def weekdays(self):
        return ['Mon', 'Tus', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    @property
    def week_date_range(self):
        from_date = self.df['date'].min()
        to_date = self.df['date'].max()
        return '%s ~ %s' % (from_date.strftime('%y-%m-%d'), to_date.strftime('%y-%m-%d'))

    @property
    def include_weekdays(self):
        include_weekdays = self.df['weekday'].unique()
        return sorted(include_weekdays, key=lambda x: self.weekdays.index(x))

    @property
    def data_list(self):
        data_df = self.df.copy()
        data_df['time_range'] = data_df['start_time'].dt.strftime('%H:%M:%S') + \
                                '~' + \
                                data_df['end_time'].dt.strftime('%H:%M:%S')
        data_df['date'] = data_df['date'].dt.strftime('%y-%m-%d')
        data_df['base_time'] = data_df['base_time'].dt.total_seconds() * 1000
        data_df['duration'] = data_df['duration'].dt.total_seconds() * 1000
        data_df.drop('start_time', axis=1, inplace=True)
        data_df.drop('end_time', axis=1, inplace=True)
        return data_df.to_dict(orient='records')

    def get_timelog_data_frame(self):
        # read csv
        csv_path = os.path.join(os.path.dirname(__file__), self.__csv_path)
        df = pd.read_csv(csv_path, index_col=0)
        df['date'] = pd.to_datetime(df['date'])
        df['base_time'] = pd.to_timedelta(df['base_time'])
        df['duration'] = pd.to_timedelta(df['duration'], unit='s')
        df['start_time'] = df['date'] + df['base_time']
        df['end_time'] = df['start_time'] + df['duration']
        df['weekday_row'] = df['date'].dt.dayofweek
        df['color'] = df['type'].apply(lambda x: self.COLOR_MAP.get(x, '#67C23A'))
        return df


if __name__ == '__main__':
    tl = TimelogModel()
    from pprint import pprint
    pprint(tl.data_list)
