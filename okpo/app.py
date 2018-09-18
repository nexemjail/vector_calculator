#!/bin/python

import flask
from flask import request

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def add():
    data = request.json
    return flask.jsonify(data['v1'] + data['v2'])


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)