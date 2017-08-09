#!/usr/env/python3
# -*- coding: UTF-8 -*-

class AppConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xh:xh@localhost/xh?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = '67gyubinjmokl,pl'

    @staticmethod
    def init_app(app):
        app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
