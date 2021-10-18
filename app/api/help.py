from flask import jsonify, request, send_from_directory
from . decorators import parameter_check
from . import api
from ..import HELP_MSG_PATH
import json

AV_EP = ["upload", "preview", "download", "stats", "filters"]
AV_FILTERS = ["canny", "greyscale", "laplacian", "gauss"]

@api.route('/help/', methods=['GET'])
@api.route('/help/<endpts>/', methods=['GET'])
@api.route('/help/filters/<filter_type>/', methods=['GET'])
@parameter_check(req_c_type='application/json')
def help(endpts=None, filter_type=None):
    if endpts and endpts in AV_EP:
        return jsonify(load_json_from_val(endpts)), 200
    elif filter_type and filter_type in AV_FILTERS:
        return jsonify(load_json_from_val(filter_type)), 200
    else:
        return jsonify(load_json_from_val('help')), 200


def load_json_from_val(val):
    f = open(HELP_MSG_PATH+f'/{val}.json')
    return json.load(f)
