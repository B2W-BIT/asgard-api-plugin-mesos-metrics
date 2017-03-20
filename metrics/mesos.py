from .config import MESOS_URL
from requests import get
from collections import defaultdict

MESOS_STATE = None

def get_state(use_cache=True):
    global MESOS_STATE

    if use_cache and MESOS_STATE:
        return MESOS_STATE

    MESOS_STATE = get("{}/state".format(MESOS_URL)).json()

    return MESOS_STATE

def get_slaves_attr():
    attrs = defaultdict(set)

    for slave in get_state()['slaves']:
        for attr in slave['attributes']:
            attrs[attr].add(slave['attributes'][attr])

    for attr in attrs:
        attrs[attr] = list(attrs[attr])

    return dict(attrs)

def get_slaves_with_attr(attrs):
    slaves = []

    for slave in get_state()['slaves']:
        intersection = dict(set(slave['attributes'].items()).intersection(set(attrs.items())))

        if intersection != attrs:
            continue

        slaves.append(slave)

    return slaves

def get_slaves_attr_usage(attrs):
    slaves = get_slaves_with_attr(attrs)
    usage = 0

    total_availble_cpu = 0
    total_availble_ram = 0

    total_used_cpu = 0
    total_used_ram = 0

    for slave in slaves:
        total_availble_cpu = total_availble_cpu + slave["resources"]['cpus']
        total_availble_ram = total_availble_ram + slave["resources"]['mem']

        total_used_cpu = total_used_cpu + slave["used_resources"]['cpus']
        total_used_ram = total_used_ram + slave["used_resources"]['mem']

    return {
        'cpu': round(total_used_cpu*100/total_availble_cpu),
        'ram': round(total_used_ram*100/total_availble_ram)
    }
