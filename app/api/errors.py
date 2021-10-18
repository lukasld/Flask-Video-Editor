import sys
import traceback
from flask import jsonify, request

from . import api

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message='', status_code=None):
        super().__init__()
        self.message = message
        self.path = request.path
        if status_code is None:
            self.status_code = InvalidAPIUsage.status_code

    def to_dict(self):
        rv = {}
        rv['path'] = self.path
        rv['status'] = self.status_code
        rv['message'] = self.message
        return rv


class IncorrectVideoFormat(InvalidAPIUsage):
    def __init__(self, message_id):
        super().__init__()
        self.message = self.msg[message_id]

    msg = {1:'Incorrect video type: only RGB - Type=video/mp4 allowed',
            2:'Incorrect video dimensions: only 720p supported (1280*720)'}


class InvalidFilterParams(InvalidAPIUsage):
    def __init__(self, message_id, filter_name=''):
        super().__init__()
        self.message = self.msg(message_id, filter_name)

    def msg(self, id, filter_name):
        # TODO:Lukas [07252021] messges could be stored in static files as JSON
        avail_msg = {1:'Incorrect filter parameters: should be {"fps": "<fps: float>", "filter_params":{"type":"<filter: str>"}} \
                    or for default preview, {"filter_params":{"type":""}}',
                     2:f'Incorrect filter parameters: filter does not exist, for more go to /api/v1/help/filters/',
                     3:f'Incorrect filter parameters: required parameters are missing or invalid, for more go to /api/v1/help/filters/{filter_name}/',
                     4:f'Incorrect download parameters: for more go to /api/v1/help/download/',
                     }
        return avail_msg[id]


@api.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), 400

