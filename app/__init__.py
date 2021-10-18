from flask import Flask
from config import config
from flask_caching import Cache

from flask_swagger_ui import get_swaggerui_blueprint

VIDEO_EXTENSION=None
VIDEO_WIDTH=None
VIDEO_HEIGHT=None

VIDEO_UPLOAD_PATH=None
FRAMES_UPLOAD_PATH=None 
IMG_EXTENSION=None

HELP_MSG_PATH=None

CACHE=None


def create_app(config_name):

    global VIDEO_EXTENSION
    global VIDEO_WIDTH
    global VIDEO_HEIGHT

    global VIDEO_UPLOAD_PATH
    global FRAMES_UPLOAD_PATH

    global IMG_EXTENSION
    global HELP_MSG_PATH
    global CACHE

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    cache = Cache(config={"CACHE_TYPE": "filesystem",
                          "CACHE_DIR": app.root_path + '/static/cache'})
    cache.init_app(app)

    CACHE = cache

    VIDEO_EXTENSION = app.config["VIDEO_EXTENSION"]
    VIDEO_WIDTH = int(app.config["VIDEO_WIDTH"])
    VIDEO_HEIGHT = int(app.config["VIDEO_HEIGHT"])

    IMG_EXTENSION = app.config["IMG_EXTENSION"]

    VIDEO_UPLOAD_PATH = app.root_path + '/static/uploads/videos'
    FRAMES_UPLOAD_PATH = app.root_path + '/static/uploads/frames'

    HELP_MSG_PATH = app.root_path + '/static/helpmessages'

    #TODO: video max dimensions, video max length

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/videoApi/v1')

    from .docs import swagger_ui
    app.register_blueprint(swagger_ui, url_prefix="/docs")


    return app
