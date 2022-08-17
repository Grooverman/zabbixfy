#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pyzabbix import ZabbixMetric, ZabbixSender


zabbix_server = '127.0.0.1'

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

# handle zabbix sender errors
def returnZabbixException(exception, data):
    e = exception
    d = data
    try:
        d = json.dumps(d)
    except:
        pass
    return {
        'result': type(e).__name__,
        'message': str(e),
        'affected_data': str(d)}, 400


# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Send(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        return jsonify({'message': 'Method not supported.'})

    # corresponds to POST request
    def post(self):
        data = request.get_json()
        metrics = []
        for d in data:
            if len(d) > 4:
                return {
                        'result': 'Error',
                        'message': error_text,
                        'affected_data': json.dumps(d)}, 400
            host = key = value = clock = None
            for i, v in enumerate(d):
                if i == 0:
                    host = v
                elif i == 1:
                    key = v
                elif i == 2:
                    value = v
                elif i == 3:
                    clock = v
            try:
                metric = ZabbixMetric(
                        host=host, key=key, value=value, clock=clock)
            except Exception as e:
                return returnZabbixException(e, d)
            metrics.append(metric)
        try:
            sender = ZabbixSender(zabbix_server)
            result = sender.send(metrics)
        except Exception as e:
            return returnZabbixException(e, metrics)
        return json.loads(str(result)), 201


# adding the defined resources along with their corresponding urls
api.add_resource(Send, '/')


# driver function
if __name__ == '__main__':
    app.run(debug = False)

