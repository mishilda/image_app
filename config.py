import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default'
    EXPERIMENT = os.environ.get('EXPERIMENT') or 'default'
