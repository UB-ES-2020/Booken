# file deepcode ignore E1102: shut it deepcode
from decouple import config


class Config:
    pass


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='localhost')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = "/static"
    TEMPLATE_FOLDER = "/dist"
    SECRET_KEY = config('SECRET_KEY', default='localhost')


config = {
    'production': ProductionConfig
}
