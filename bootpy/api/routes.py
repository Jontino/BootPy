from flask import request, Response, jsonify
from . import api


# GET
@api.route('/relay')
def get_devices():
    return jsonify({'devices': "#"})
