#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Flask
from mess import fun_logger, set_logger
from api_handle import api, job_api, record_api, relationship_api, token_api, volunteer_api
from auth_handle import bcrypt
from tables import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://xh:xh@localhost/xh?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api.init_app(app)
bcrypt.init_app(app)
db.init_app(app)

api.add_resource(token_api, '/api/tokens')
api.add_resource(volunteer_api, '/api/volunteers')
api.add_resource(job_api, '/api/jobs')
api.add_resource(record_api, '/api/records')
api.add_resource(relationship_api, '/api/relationship')

if __name__ == '__main__':
    set_logger('log.txt')
    app.run(debug=True)
