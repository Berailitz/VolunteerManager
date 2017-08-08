#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from .api_handle import create_api
from .auth_handle import bcrypt
from .config import AppConfig
from .main.views import create_main_blueprint
from .mess import fun_logger
from .tables import db
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    toolbar = DebugToolbarExtension(app)
    api = create_api()
    api.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    AppConfig.init_app(app)
    main_blueprint = create_main_blueprint()
    app.register_blueprint(main_blueprint)
    logging.info('%r', app.view_functions)
    logging.info('%r', app.url_map)
    return app
