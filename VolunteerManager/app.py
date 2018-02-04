"""main module including create_app()"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.contrib.fixers import ProxyFix
from .api_handle import create_api
from .auth_handle import bcrypt
from .config import AppConfig
from .main.views import create_main_blueprint
from .mess import get_current_time, set_logger
from .tables import db

def create_app(log_path='log'):
    """create initialized flask app, compatible with uwsgi"""
    if not os.path.exists(log_path):
        raise FileNotFoundError(f'Log path does not exist: `{log_path}`.')
    log_path = f'{log_path}/log_{get_current_time()}_{os.getpid()}.txt'
    set_logger(log_path)
    logging.info(f'Logging to `{log_path}`')
    app = Flask(__name__, static_folder=None)
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
