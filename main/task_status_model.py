# -*- coding: UTF-8 -*-

import os
import pandas as pd


class TaskStatusModel(object):
    def __init__(self, csv_path="../src_data/task_status.csv"):
        self.__csv_path = csv_path
        self.__df = self.get_ts_data_frame()

    @property
    def df(self):
        return self.__df

    @property
    def status_count(self):
        count_dict = self.df['status'].value_counts().to_dict()
        return [{'name': name, 'value': value} for name, value in count_dict.items()]

    @property
    def status_list(self):
        return list(self.df['status'].unique())

    @property
    def class_count(self):
        count_dict = self.df['class'].value_counts().to_dict()
        return [{'name': name, 'value': value} for name, value in count_dict.items()]

    @property
    def class_list(self):
        return list(self.df['class'].unique())

    def get_color_list(self, status_list):
        status_colors = {
            "rdy": "#F56C6C",
            "ip": "#909399",
            "cbb": "#409EFF",
            "rvw": "#E6A23C",
            "apv": "#67C23A",
            "inprogress": "#909399",
            "approve": "#67C23A",
            "not_started": "#F56C6C",
        }
        return list(map(lambda x: status_colors.get(x), status_list))

    def get_ts_data_frame(self):
        # read csv
        csv_path = os.path.join(os.path.dirname(__file__), self.__csv_path)
        return pd.read_csv(csv_path)


if __name__ == '__main__':
    ts = TaskStatusModel()
    print(ts.class_list+ts.status_list)
    print(ts.get_color_list(ts.class_list+ts.status_list))

