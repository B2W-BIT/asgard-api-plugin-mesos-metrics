
import requests

from asgard.sdk import mesos

from metrics import config

def get_mesos_slaves():
    leader_address = mesos.get_mesos_leader_address()
    url = f"{leader_address}/slaves"
    config.logger.debug({"action": "pre-fetch", "fetch-url": url})
    response = requests.get(url, timeout=2)
    config.logger.debug({"action": "post-fetch", "fetch-url": url, "fetch-status": response.status_code})
    return response.json()

def get_mesos_tasks():
    leader_address = mesos.get_mesos_leader_address()
    url = f"{leader_address}/tasks?limit=-1"
    config.logger.debug({"action": "pre-fetch", "fetch-url": url})
    response = requests.get(url, timeout=2)
    config.logger.debug({"action": "post-fetch", "fetch-url": url, "fetch-status": response.status_code})
    return response.json()
