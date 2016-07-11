import csv
import json
import math
import nltk
from nltk.corpus import wordnet


class orgnization:
    def __init__(self,data):
        self.stage_num = -1
        self.data = data


    def get_data(self):
        return self.data

    def get_stage_num(self):
        return self.stage_num

    def set_stage_num(self, stage):
        self.stage_num = stage

class database():

    def __init__(self):
        self.data_list = []
        with open('data.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                single_data = orgnization(row)
                self.data_list.append(single_data)

    def get_colums(self):
        col_name = ['','','','','','']

    def get_raw_data(self):
        raw_data = []
        for single_data in self.data_list:
            if single_data.get_stage_num() == -1:
                raw_data.append(single_data.get_data())
        return raw_data


    def fileter_cato(self, col_list, stage):
        current_data_list = self.data_list
        for single_data in current_data_list:
            if single_data.get_stage_num() != -1:
                continue
            stage_num = stage
            for col_name in col_list:
                if single_data.get_data().get(col_name) == '1':
                    stage_num = -1
            if stage_num != -1:
                single_data.set_stage_num(stage)

    def filter_col(self, col_name, col_value, stage):
        current_data_list = self.data_list
        for single_data in current_data_list:
            if single_data.get_stage_num() != -1:
                continue
            if single_data.get_data().get(col_name) not in col_value:
                single_data.set_stage_num(stage)

    def check_colum(self, col_name, col_val):
        current_data = self.get_raw_data()
        flag = False
        for single_data in current_data:
            if single_data.get(col_name) == col_val:
                flag = True
        return flag


    def get_max_stage_num(self):
        curret_data = self.data_list
        max = -1
        for single_data in curret_data:
            if single_data.get_stage_num() > max:
                max = single_data.get_stage_num()
        return max

    def restore_data(self, stage_num):
        for single_data in self.data_list:
            if single_data.get_stage_num() == stage_num:
                single_data.set_stage_num(-1)
#
#
# a = database()
#
# a.filter_col('Cost',['Paid','Free'])
# a.fileter_cato(['Legal', 'Finance'])


def get_col_by_entropy(col_name_list, data):
    col_entroy = {}
    data_len = len(data)
    for col_name in col_name_list:
        col_entroy[col_name] = {}
    for single_data in data:
        for col_name in col_name_list:
            val = single_data.get(col_name)
            if val not in col_entroy[col_name]:
                col_entroy[col_name][val] = 0
            col_entroy[col_name][val] += 1
    max_entropy = 0
    max_col_name = None
    for col_name, col_val in col_entroy.items():
        current_entropy = 0
        for val,num in col_val.items():
            current_entropy -= (float(num)/data_len)*math.log((float(num)/data_len))
        if current_entropy > max_entropy:
            max_entropy = current_entropy
            max_col_name = col_name
    return max_col_name