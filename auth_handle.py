#!/usr/env/python3
# -*- coding: UTF-8 -*-

import datetime
import logging
from flask_bcrypt import Bcrypt
from mess import generate_random_string
from sql_handle import get_tokens, check_NoResultFound
from tables import db

bcrypt = Bcrypt()
def check_token(token):
    try:
        admin = get_tokens({'token': token, 'query_type': 'one'}, ['token'])
        logging.info('%r: token: %r.', admin, token)
        if datetime.datetime.now() > admin.login_time + datetime.timedelta(days=7):
            admin.token = ''
            return False
        else:
            return admin
    except Exception as e:
        if not check_NoResultFound(e, {'token': token, 'query_type': 'one'}):
            logging.exception(e)
            raise e
        return False

def check_password(username, password):
    try:
        admin = get_tokens({'username': username, 'query_type': 'one'}, ['username'])
        logging.info('username: %r, password: %r.', username, password)
        if bcrypt.check_password_hash(admin.password, password):
            return admin
    except Exception as e:
        if not check_NoResultFound(e, {'username': username, 'query_type': 'one'}):
            logging.exception(e)
            raise e
        return False

def authenticate(**credential):
    if credential['token']:
        return check_token(credential['token'])
    elif credential['username'] and credential['password']:
        return check_password(credential['username'], credential['password'])
    else:
        return False

def update_token(**credential):
    admin = authenticate(**credential)
    if admin:
        admin.token = generate_random_string(64)
        db.session.commit()
        return admin.token
    else:
        return None
