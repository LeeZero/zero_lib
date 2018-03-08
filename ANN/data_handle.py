#!/usr/bin/python2.7
# coding=utf-8

from ann import NeuralNetwork
import numpy as np
from util.tool_mongo_client import ToolMongoClient


class DataHandle(object):
    def __init__(self, **kwargs):
        self._quote_collection_name = kwargs.get("quote_collection")
        self._qoute_mongo_client = ToolMongoClient(kwargs.get("base_cfg_file", "mongo.conf"))
        self._class_type = kwargs.get("class_type")
        self._time_class = kwargs.get("time_class")
        self.X, self.y = self.__get_data()
        self.ann = NeuralNetwork([4, 3, 4], "tanh")

    def __get_data(self):
        x_list, y_list = [], []
        _filter = {"class_type": self._class_type, "time_class": self._time_class}
        for data in self._qoute_mongo_client.find_many(self._quote_collection_name, filter=_filter):
            tmp = [data.get("open_price"), data.get("close_price"), data.get("max_price"), data.get("min_price")]
            x_list.append(tmp)
        return np.array([x_list]), np.array([y_list])



