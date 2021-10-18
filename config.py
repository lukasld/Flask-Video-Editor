import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    """
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_CONFIG = os.environ.get('FLASK_CONFIG')

    VIDEO_EXTENSION = os.environ.get('VIDEO_EXTENSION')
    VIDEO_WIDTH = os.environ.get('VIDEO_WIDTH')
    VIDEO_HEIGHT = os.environ.get('VIDEO_HEIGHT')

    IMG_EXTENSION = os.environ.get('IMG_EXTENSION')


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    """
    """
    DEBUG = True

config = {
        'development': DevelopmentConfig,
        'default': DevelopmentConfig
}
