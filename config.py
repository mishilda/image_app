import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default'
    VAR1 = 'original, output sat 1.1, output sat 1.5' 
    VAR2 = 'original, output wp 500, output wp 1000'
    RESP_DICT = {
        '++left': -2,
        '+left': -1,
        'indifferent': 0,
        '+right': 1,
        '++right': 2,
    }
