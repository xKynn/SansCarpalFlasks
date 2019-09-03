import configparser
import copy
import os

_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
_par = os.path.abspath(os.path.join(_dir, os.pardir))

DEFAULT = configparser.ConfigParser()
DEFAULT.read(f'{_dir}\\data\\defaultconf.ini')


def _fresh_config():
    config = copy.deepcopy(DEFAULT)
    with open(f'{_par}\\config.ini', 'w') as file:
        config.write(file)
    return config


def get_config():
    conf = configparser.ConfigParser()
    conf.read(f"{_par}\\config.ini")
    if not conf:
        conf = _fresh_config()
    return conf
