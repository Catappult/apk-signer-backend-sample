from flask import jsonify
from flask_restx import Resource


class StatusEndpoint(Resource):
    def __init__(self, self_api, *args, **kwargs):
        super().__init__(self_api, *args, **kwargs)

    def get(self):
        return jsonify(status="OK")
