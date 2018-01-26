import json
import os
from typing import Dict

CURRENT_DIR = os.path.dirname(__file__)

def get_fixture(file_name: str) -> Dict:
    with open(os.path.join(CURRENT_DIR, file_name)) as fp:
        return json.load(fp)

def with_json_fixture(fixture_path):
    def wrapper(func):
        def decorator(self):
            fixture = get_fixture(fixture_path)
            return func(self, fixture)
        return decorator
    return wrapper

SLAVES_STATE = {
    "slaves":[
        {
            "resources":{"disk":600000.0,"mem": 16000.0,"gpus":0.0,"cpus":4.0},
            "used_resources":{"disk":0.0,"mem":8000.0,"gpus":0.0,"cpus":2.4},
            "attributes":{"dc":"bit","server":"slave0"},
            "active": True
        },
        {
            "resources":{"disk":400000.0,"mem": 8000.0,"gpus":0.0,"cpus":8.0},
            "used_resources":{"disk":0.0,"mem":8000.0,"gpus":0.0,"cpus":3.6},
            "attributes":{"dc":"bit","server":"slave1"},
            "active": True
        },
    ]
}
