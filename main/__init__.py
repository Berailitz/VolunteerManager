#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Blueprint
main_blueprint = Blueprint('main', __name__, template_folder='templates')
from . import views

def create_main_blueprint(app):
    app.register_blueprint(main_blueprint)
