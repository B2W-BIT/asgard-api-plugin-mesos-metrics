from flask import Flask, Response, request
from metrics import mesos, config
from json import dumps

app = Flask(__name__)

from functools import wraps
from flask import request, Response


def check_auth(username, password):
    return username == config.BASICAUTH_USERNAME and password == config.BASICAUTH_PASSWORD

def authenticate():
    return Response(
        'Forbidden',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/attrs')
@requires_auth
def attrs():
    slaves_state = mesos.get_mesos_slaves()
    return Response(
        dumps(mesos.get_slaves_attr(slaves_state)),
        mimetype='application/json'
    )

@app.route('/slaves-with-attrs')
@requires_auth
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
@requires_auth
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

if __name__ == '__main__':
    app.run()
