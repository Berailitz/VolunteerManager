"""main module including create_app()"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from .api_handle import create_api
from .auth_handle import bcrypt
from .config import AppConfig
from .main.views import create_main_blueprint
from .tables import db

def create_app():
    """create initialized flask app, compatible with uwsgi"""
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    toolbar = DebugToolbarExtension()
    api = create_api()
    api.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    app_config = AppConfig()
    app_config.init_app(app)
    toolbar.init_app(app)
    main_blueprint = create_main_blueprint()
    app.register_blueprint(main_blueprint)
    logging.info('%r', app.view_functions)
    logging.info('%r', app.url_map)
    return app
