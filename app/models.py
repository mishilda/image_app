from uuid import uuid4
from datetime import datetime
from random import shuffle
import json
import os

class Experiment(object):
    def __init__(self, data):
        if type(data) in [bytes, str, bytearray]:
            data = self.load(data)
        self.exp_uuid = data.get('exp_uuid', '')
        self.create_datetime = data.get('create_datetime', '')
        self.dataset = data.get('dataset', '')
        self.amount_of_pic = int(data.get('amount_of_pic', ''))
        self.time_to_response = data.get('time_to_response', '') 
        self.config_name = data.get('config_name', '')
    
    def save(self):
        save_dict = {}
        save_dict['exp_uuid'] = self.exp_uuid or str(uuid4())
        save_dict['create_datetime'] = self.create_datetime or datetime.utcnow().isoformat()
        save_dict['dataset'] = self.dataset
        save_dict['amount_of_pic'] = self.amount_of_pic
        save_dict['time_to_response'] = self.time_to_response
        save_dict['config_name'] = self.config_name
        data = json.dumps(save_dict)
        filename = "./app/exp_config/" + (save_dict['config_name'] if save_dict['config_name'] else save_dict['exp_uuid'])
        with open(filename, 'w') as new_file:
            new_file.write(data)
        
    def load(self, json_data):
        data = json.loads(json_data)
        return data
    
    def set_current(self):
        self.config_name = 'current'
        self.save()

    def load_dataset(self):
        dirs = self.dataset.split(',')        
        dataset = []
        ph_names = []
        
        ph_names = os.listdir('./app/static/original/')
        for ph_name in ph_names:
            item = {}
            for d in dirs:
                path = './app/static/' + d.strip() + '/'
                file_names = os.listdir(path)
                for f_name in file_names:
                    if ph_name.split('.')[0] in f_name:
                        item[d] = 'static/' + d.strip() + '/' + f_name
                        break
            dataset.append(item)
        return dataset

        # for d in dirs:
        #     path = './app/pic/' + d.strip() + '/'
        #     names = os.listdir(path)
        #     dataset.append(names)
        # check_len = len(dataset[0])
        # for i in dataset:
        #     if len(i) != check_len:
        #         return None
        # return dataset

    def randomize_dataset(self):
        dataset = self.load_dataset()
        items = []
        shuffle(dataset)
        for i in range(self.amount_of_pic):
            items.append(dataset[i])
        return items



class Interviewee():
    name = None
    age = None
    gender = None
    education = None