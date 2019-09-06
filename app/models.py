from uuid import uuid4
from datetime import datetime
from random import shuffle
import pandas as pd
import json
import os
import os.path as p

class Experiment(object):
    def __init__(self, data):
        if type(data) in [bytes, str, bytearray]:
            data = self._load(data)
        self.create_datetime = data.get('create_datetime', datetime.utcnow().isoformat())
        self.left_dir = data.get('left_dir')
        self.center_dir = data.get('center_dir')
        self.right_dir = data.get('right_dir')
        self.width = data.get('width')
        #self.dataset = data.get('dataset', '')
        #self.rel_dataset = p.relpath(self.dataset, './app/static')
        self.repetitions = int(data.get('repetitions', '')) or 1
        self.time_to_response = data.get('time_to_response', '')
        self.config_name = data.get('config_name', '')
        #self.original_w = data.get('original_w', '')
        #self.left_w = data.get('left_w', '')
        #self.right_w = data.get('right_w', '')
        self.task = data.get('task', '')
        #self.with_comments = True if data.get('with_comments', False) else False

    def save(self):
        save_dict = {}
        save_dict['create_datetime'] = self.create_datetime or datetime.utcnow().isoformat()
        #save_dict['dataset'] = self.dataset
        save_dict['repetitions'] = self.repetitions
        save_dict['time_to_response'] = self.time_to_response
        save_dict['config_name'] = self.config_name
        save_dict['center_dir'] = self.center_dir
        save_dict['left_dir'] = self.left_dir
        save_dict['right_dir'] = self.right_dir
        save_dict['width'] = self.width
        save_dict['task'] = self.task
       # save_dict['with_comments'] = self.with_comments
        data = json.dumps(save_dict)
        filename = os.path.join("./app/exp_config/", save_dict['config_name'])
        with open(filename, 'w') as new_file:
            new_file.write(data)

    def _load(self, json_data):
        data = json.loads(json_data)
        return data

    # def load_dataset(self):
    #     dirs = self.dataset.split(',')
    #     dataset = []
    #     ph_names = []

    #     ph_names = os.listdir('./app/static/original/')
    #     for ph_name in ph_names:
    #         item = []
    #         for d in dirs:
    #             path = './app/static/' + d.strip() + '/'
    #             file_names = os.listdir(path)
    #             for f_name in file_names:
    #                 if ph_name.split('.')[0] in f_name:
    #                     item.append('static/' + d.strip() + '/' + f_name)
    #                     break
    #         dataset.append(item)
    #     return dataset

        # for d in dirs:
        #     path = './app/pic/' + d.strip() + '/'
        #     names = os.listdir(path)
        #     dataset.append(names)
        # check_len = len(dataset[0])
        # for i in dataset:
        #     if len(i) != check_len:
        #         return None
        # return dataset

    def load_dataset(self, reverse=False):
        left = os.listdir(p.join('./app/static', self.left_dir))
        center = os.listdir(p.join('./app/static', self.center_dir))
        right = os.listdir(p.join('./app/static', self.right_dir))
        dirs = [left, center, right]
        for d in dirs:
            d.sort()
        items = []
        for i in range(len(left)):
            item = {
                'left': p.join('static', self.left_dir, left[i]),
                'center': p.join('static', self.center_dir, center[i]),
                'right': p.join('static', self.right_dir, right[i])
            }
            items.append(item)
        return items


    def randomize_dataset(self, reverse=False):
        dataset = self.load_dataset(reverse)
        items = dataset * self.repetitions
        shuffle(items)
        return items

    # def load_dataset(self, reverse=False):
    #     data = pd.read_csv(self.dataset, sep=",")
    #     column = ['orig', 'left', 'right']
    #     reverse_col = ['orig', 'right', 'left']
    #     for col in column:
    #         if col not in data.columns:
    #             return None
    #     for col in data.columns:
    #         if data[data[col].isnull()].shape[0]:
    #             return None

        if reverse:
            column = reverse_col
        items = []
        for i in range(data.shape[0]):
            item = []
            for col in column:
                item.append(data[col][i])
            items.append(item)
        return items
