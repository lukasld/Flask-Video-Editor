from flask import redirect, url_for, jsonify
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

@main.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify(error=str(e)), 405


