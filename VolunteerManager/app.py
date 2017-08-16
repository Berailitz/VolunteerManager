"""main module including create_app()"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.contrib.fixers import ProxyFix
from .api_handle import create_api
from .auth_handle import bcrypt
from .config import AppConfig
from .main.views import create_main_blueprint
from .mess import set_logger
from .tables import db

def create_app():
    """create initialized flask app, compatible with uwsgi"""
    set_logger('log/log.txt')
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
    app.wsgi_app = ProxyFix(app.wsgi_app)
    logging.info('%r', app.view_functions)
    logging.info('%r', app.url_map)
    return app
