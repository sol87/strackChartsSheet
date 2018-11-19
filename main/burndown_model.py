# -*- coding: UTF-8 -*-
# Copyright (c) 2018 CineUse

import os
import datetime as dt
import pandas as pd
import numpy as np


class BurndownModel(object):
    def __init__(self, csv_path="../src_data/burndown_data.csv", start_date="2018-06-24", due_date="2019-2-18"):
        self.__csv_path = csv_path
        self.__df = self.get_burndown_data_frame()
        self.__date_list = []
        self.__completion_list = []
        self.__ideal_list = []
        self.__start_date = start_date
        self.__due_date = due_date

    @property
    def df(self):
        return self.__df

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        self.__start_date = value
        self.reset()

    @property
    def due_date(self):
        return self.__due_date

    @due_date.setter
    def due_date(self, value):
        self.__due_date = value
        self.reset()

    @property
    def date_list(self):
        if not self.__date_list:
            self.__date_list = [d.strftime("%Y-%m-%d") for d in
                                pd.date_range(self.__start_date, self.__due_date, freq="D")]
        return self.__date_list

    @property
    def completion_list(self):
        if not self.__completion_list:
            self.__completion_list = self.df["completion"].tolist()
        return self.__completion_list

    @property
    def ideal_list(self):
        if not self.__ideal_list:
            total = self.completion_list[0]
            self.__ideal_list = np.arange(total, 0, -float(total) / (len(self.date_list)-1)).astype(np.int16).tolist() + [0]
        return self.__ideal_list

    @property
    def loss_list(self):
        loss_array = np.asarray(self.completion_list) - np.asarray(self.ideal_list[:len(self.completion_list)])
        return loss_array.tolist()

    def get_burndown_data_frame(self):
        # read csv
        csv_path = os.path.join(os.path.dirname(__file__), self.__csv_path)
        return pd.read_csv(csv_path, names=["date", "completion"])

    def reset(self, new_path=None):
        if new_path:
            self.__csv_path = new_path
        # reset all attributes
        self.__df = self.get_burndown_data_frame()
        self.__date_list = []
        self.__completion_list = []
        self.__ideal_list = []


if __name__ == '__main__':
    bd = BurndownModel()
    print(len(bd.date_list))
    print("*" * 10)
    print(len(bd.completion_list))
    print("*" * 10)
    print(len(bd.ideal_list))
