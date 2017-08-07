#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Flask
from api_handle import api, init_api, job_api, record_api, relationship_api, token_api, volunteer_api
from auth_handle import bcrypt
from config import AppConfig
from tables import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    api.init_app(app)
    init_api(api)
    bcrypt.init_app(app)
    db.init_app(app)
    AppConfig.init_app(app)
    return app
