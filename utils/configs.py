import json
import copy
import os

_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
_par = os.path.abspath(os.path.join(_dir, os.pardir))

with open(f"{_dir}\\data\\defaultconf.json") as def_file:
    DEFAULT = json.load(def_file)


def _fresh_config():
    config = copy.deepcopy(DEFAULT)
    with open(f'{_par}\\config.json', 'w') as file:
        json.dump(config, file)
    return config


def get_config():
    if os.path.isfile(f"{_par}\\config.json"):
        with open(f"{_par}\\config.json") as conf_file:
            conf = json.load(conf_file)
    else:
        conf = _fresh_config()
    return conf
