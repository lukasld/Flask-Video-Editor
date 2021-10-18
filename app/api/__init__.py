from flask import Blueprint

api = Blueprint('videoApi', __name__)

from . import videoApi, errors, help
