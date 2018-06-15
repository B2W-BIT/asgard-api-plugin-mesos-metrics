from metrics import config
from metrics.util import get_mesos_slaves, get_mesos_tasks
from requests import get
from collections import defaultdict

CHRONOS_TASK_PREFIX = "ct"
MESOS_TASK_RUNNING = "TASK_RUNNING"

def _get_task_namespace(task_name):
    ns = task_name.split("_")[0]
    if task_name.startswith(CHRONOS_TASK_PREFIX):
        ns = "other"
    return f"{ns}_"

def get_tasks():
    all_tasks = get_mesos_tasks()
    counts = defaultdict(int)
    for task in all_tasks['tasks']:
        ns = _get_task_namespace(task['id'])
        counts['total'] += 1
        counts[task['state'].lower()] += 1

        state = task['state']
        if state == MESOS_TASK_RUNNING:
            counts[f"{ns}{state.lower()}"] += 1

        counts[f"{ns}{MESOS_TASK_RUNNING.lower()}"]

    return counts

def get_slaves_attr(slaves_state):
    attrs = defaultdict(set)

    for slave in slaves_state['slaves']:
        for attr in slave['attributes']:
            attrs[attr].add(slave['attributes'][attr])

    for attr in attrs:
        attrs[attr] = list(attrs[attr])

    return dict(attrs)

def get_slaves_with_attr(slaves_state, attrs):
    slaves = []

    for slave in slaves_state['slaves']:
        intersection = dict(set(slave['attributes'].items()).intersection(set(attrs.items())))

        if intersection != attrs:
            continue

        slaves.append(slave)

    return slaves

def get_attr_usage(slaves_state, attrs):
    slaves = get_slaves_with_attr(slaves_state, attrs)

    usage = 0

    cpu_total = 0
    ram_total = 0

    cpu_used = 0
    ram_used = 0

    for slave in slaves:
        cpu_total = cpu_total + slave["resources"]['cpus']
        ram_total = ram_total + slave["resources"]['mem']

        cpu_used = cpu_used + slave["used_resources"]['cpus']
        ram_used = ram_used + slave["used_resources"]['mem']

    ram_total = round(ram_total/1000)
    ram_used = round(ram_used/1000)

    return {
        'cpu_total': cpu_total,
        'ram_total': ram_total,
        'cpu_used': cpu_used,
        'ram_used': ram_used,
        'cpu_pct': round(cpu_used*100/(cpu_total or 1), 1),
        'ram_pct': round(ram_used*100/(ram_total or 1), 1)
    }
