from flask import Blueprint, Response, request
from metrics import mesos, config
from json import dumps

app = Blueprint(__name__, __name__)

@app.route('/attrs')
def attrs():
    slaves_state = mesos.get_mesos_slaves()
    return Response(
        dumps(mesos.get_slaves_attr(slaves_state)),
        mimetype='application/json'
    )

@app.route('/slaves-with-attrs')
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

@app.route('/attr-usage')
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

