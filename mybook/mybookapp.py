# coding: utf-8

import dataset
import logging
from flask import Flask
from logging import handlers, Formatter
from .config import default


people = {}


def create_app():
    app = Flask("mybook")
    init_logging_handler(app)
    load_config(app)
    load_database(app)
    load_blueprints(app)
    return app


def init_logging_handler(app):
    handler = handlers.RotatingFileHandler('mybook.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))
    app.logger.addHandler(handler)


def load_config(app):
    app.config.from_object(default)
    app.config.from_envvar('TODO_SETTINGS', silent=True)


def load_database(app):
    db = dataset.connect(app.config['DATABASE'])
    global people
    people = db['people']


def load_blueprints(app):
    from api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
