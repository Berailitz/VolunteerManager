#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Flask
from api_handle import api, init_api
from auth_handle import bcrypt
from config import AppConfig
from main import main_blueprint
from tables import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    api.init_app(app)
    init_api(api)
    bcrypt.init_app(app)
    db.init_app(app)
    AppConfig.init_app(app)
    app.register_blueprint(main_blueprint)
    return app
