import logging.config

import os
from parking_api.config import config as app_config
from parking_api.api.endpoints.rates import ns as rates_namespace
from parking_api.api.restx import api
from parking_api.database import db
from flask import Flask, Blueprint

logging_file_postfix = os.getenv("APP_ENV", "")
if logging_file_postfix != "":
    logging_file_postfix = '_' + logging_file_postfix
logging_conf_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), f"../../../logging{logging_file_postfix}.conf"))

logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = app_config.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = app_config.RESTX_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTX_VALIDATE'] = app_config.RESTX_VALIDATE
    flask_app.config['RESTX_MASK_SWAGGER'] = app_config.RESTX_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = app_config.ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(rates_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app_config.SQLALCHEMY_TRACK_MODIFICATIONS
    initialize_app(app)

    return app
