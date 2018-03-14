# _*_ coding:utf-8 _*_

from flask import Flask
from config import config

from logbook import Logger

from .lib.mysql import MySQLClient
from .log import setup_logger


mysql_client = MySQLClient()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    setup_logger(app.config)
    log = Logger("APP")
    log.debug(app.config)

    log.debug(mysql_client.init_app(app))

    from app.api import api as api_blueprint
    
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
