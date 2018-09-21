from json import dumps
import json

import requests
from flask import Blueprint, Response, request

from metrics import mesos, config
from asgard.sdk import mesos as mesos_asgard_sdk
from asgard.sdk import options

mesos_metrics_blueprint = Blueprint(__name__, __name__)

def asgard_api_plugin_init(**kwargs):
    config.logger = kwargs.get("logger", config.logger)
    return {
        'blueprint': mesos_metrics_blueprint
    }

@mesos_metrics_blueprint.route('/attrs/count')
def attrs_count():
    config.logger.debug("Counting attrs")
    slaves_state = mesos.get_mesos_slaves()
    slaves_attrs = mesos.get_slaves_attr(slaves_state)
    return Response(
        dumps({'total_attrs': len(slaves_attrs.keys())}),
        mimetype='application/json'
    )

@mesos_metrics_blueprint.route('/tasks/count')
def tasks_count():
    config.logger.debug("Counting tasks")
    mesos_tasks = mesos.get_tasks()
    return Response(
        dumps(mesos_tasks),
        mimetype='application/json'
    )

@mesos_metrics_blueprint.route('/attrs')
def attrs():
    config.logger.debug("Reading attrs")
    slaves_state = mesos.get_mesos_slaves()
    return Response(
        dumps(mesos.get_slaves_attr(slaves_state)),
        mimetype='application/json'
    )


@mesos_metrics_blueprint.route('/slaves-with-attrs/count')
def slaves_with_attrs_count():
    slaves_state = mesos.get_mesos_slaves()
    result = mesos.get_slaves_with_attr(
        slaves_state,
        dict(request.args.items())
    )
    return Response(
        dumps({'total_slaves': len(result)}),
        mimetype='application/json'
    )

@mesos_metrics_blueprint.route('/slaves-with-attrs')
def slaves_with_attrs():
    slaves_state = mesos.get_mesos_slaves()
    result = mesos.get_slaves_with_attr(
        slaves_state,
        dict(request.args.items())
    )
    return Response(
        dumps(result),
        mimetype='application/json'
    )

@mesos_metrics_blueprint.route('/attr-usage')
def slaves_attr_usage():
    slaves_state = mesos.get_mesos_slaves()
    result = mesos.get_attr_usage(
        slaves_state,
        dict(request.args.items())
    )
    return Response(
        dumps(result),
        mimetype='application/json'
    )

@mesos_metrics_blueprint.route("/masters/alive")
def masters_alive():
    mesos_addresses = options.get_option("MESOS", "ADDRESS")
    result = {addr: int(mesos_asgard_sdk.is_master_healthy(addr)) for addr in mesos_addresses}
    all_ok = all([result[key] for key in result.keys()])
    masters_down = len(list(filter(lambda r: r[1] == 0, result.items())))

    result['all_ok'] = int(all_ok)
    result['masters_down'] = masters_down
    return Response(
        dumps(result),
        mimetype='application/json'
    )



def filter_mesos_metrics(server_address, prefix):
    metrics_data = requests.get(f"{server_address}/metrics/snapshot").json()
    filtered_metrics = {}
    for data_key, data_value in metrics_data.items():
        if data_key.startswith(prefix):
            filtered_metrics[data_key] = data_value
    return filtered_metrics

@mesos_metrics_blueprint.route("/leader")
def leader_metrics():
    prefix = request.args.get("prefix", "")
    server_address = mesos_asgard_sdk.get_mesos_leader_address()
    filtered_metrics = filter_mesos_metrics(server_address, prefix)
    return Response(json.dumps(filtered_metrics), mimetype='application/json')

@mesos_metrics_blueprint.route("/master/<string:server_ip>")
def master_metrics(server_ip):
    prefix = request.args.get("prefix", "")
    filtered_metrics = filter_mesos_metrics(f"http://{server_ip}:5050", prefix)
    return Response(json.dumps(filtered_metrics), mimetype='application/json')

@mesos_metrics_blueprint.route("/slave/<string:server_ip>")
def slave_metrics(server_ip):
    prefix = request.args.get("prefix", "")
    filtered_metrics = filter_mesos_metrics(f"http://{server_ip}:5051", prefix)
    return Response(json.dumps(filtered_metrics), mimetype='application/json')

