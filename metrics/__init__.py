from json import dumps
import json

import requests
from flask import Blueprint, Response, request

from metrics import mesos, config

mesos_metrics_blueprint = Blueprint(__name__, __name__)

def asgard_api_plugin_init():
    return {
        'blueprint': mesos_metrics_blueprint
    }

@mesos_metrics_blueprint.route('/attrs')
def attrs():
    slaves_state = mesos.get_mesos_slaves()
    return Response(
        dumps(mesos.get_slaves_attr(slaves_state)),
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


def filter_mesos_metrics(server_ip, port, prefix):
    metrics_data = requests.get(f"http://{server_ip}:{port}/metrics/snapshot").json()
    filtered_metrics = {}
    for data_key, data_value in metrics_data.items():
        if data_key.startswith(prefix):
            filtered_metrics[data_key] = data_value
    return filtered_metrics

@mesos_metrics_blueprint.route("/master/<string:server_ip>")
def master_metrics(server_ip):
    prefix = request.args.get("prefix", "")
    filtered_metrics = filter_mesos_metrics(server_ip, 5050, prefix)
    return Response(json.dumps(filtered_metrics), mimetype='application/json')

@mesos_metrics_blueprint.route("/slave/<string:server_ip>")
def slave_metrics(server_ip):
    prefix = request.args.get("prefix", "")
    filtered_metrics = filter_mesos_metrics(server_ip, 5051, prefix)
    return Response(json.dumps(filtered_metrics), mimetype='application/json')

