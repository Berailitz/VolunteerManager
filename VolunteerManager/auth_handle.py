'''handle authentication'''
#!/usr/env/python3
# -*- coding: UTF-8 -*-

import datetime
import functools
import logging
from flask import redirect, request, make_response
from flask_bcrypt import Bcrypt
from flask_restful import reqparse
from flask_sqlalchemy import orm
from .config import AppConfig
from .mess import fun_logger, generate_random_string
from .restful_helper import get_arg
from .sql_handle import get_tokens
from .tables import db

bcrypt = Bcrypt()

def check_token(token):
    '''PRIVATE: check and clear overdue token, return original <admin> or None for invalid or OVERDUE ones'''
    try:
        admin = get_tokens({'token': token, 'query_type': 'one'}, ['token'])
        # logging.info('%r: token: %r.', admin, token)
        if datetime.datetime.now() > admin.login_time + datetime.timedelta(days=7):
            admin.token = ''
            return None
        return admin
    except orm.exc.NoResultFound as identifier:
        logging.exception('%r: %r', identifier, identifier.args)
        return None

def check_password(username, password):
    '''PRIVATE: check password, return original <admin> or None'''
    try:
        admin = get_tokens({'username': username, 'query_type': 'one'}, ['username'])
        # logging.info('username: %r, password: %r.', username, password)
        if bcrypt.check_password_hash(admin.password, password):
            return admin
    except orm.exc.NoResultFound as identifier:
        logging.exception('%r: %r', identifier, identifier.args)
        return None

def authenticate(**credential):
    '''PRIVATE: check token and then password, return original <admin> or None'''
    if 'token' in credential and credential['token']:
        return check_token(credential['token'])
    elif 'username' in credential and 'password' in credential and credential['username'] and credential['password']:
        return check_password(credential['username'], credential['password'])
    return None

def get_current_user(**credential):
    '''check token and then password from dict, return <admin> with token UPDATED or None, invoking `authenticate`'''
    admin = authenticate(**credential)
    if admin:
        admin.token = generate_random_string(AppConfig.TOKEN_LENGTH)
        db.session.commit()
        return admin
    return None

def check_cookie(current_request):
    '''check token in cookie of current_request, return <admin> with token UPDATED or None, invoking `authenticate`'''
    try:
        current_token = current_request.cookies.get('token')
        current_user = authenticate(token=current_token)
        if current_user:
            current_user.token = generate_random_string(AppConfig.TOKEN_LENGTH)
            db.session.commit()
            return current_user
        return None
    except KeyError as identifier:
        logging.warning('%r', identifier)
        return None

# @fun_logger('login')
def admin_only(public_view='/'):
    '''decorated functions should NEVER change column `tokens`, redirect the unauthorized to `public_view`, invoking `check_cookie`'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            '''update token or set invalid token to ``'''
            admin = check_cookie(request)
            if admin:
                response = func(*args, **kw)
                response.set_cookie('token', admin.token, max_age=604800, secure=True)
            else:
                response = make_response(redirect(public_view))
                response.set_cookie('token', '', max_age=604800, secure=True)
            return response
        return wrapper
    return decorator

# @fun_logger('login')
def guest_only(restricted_view='/record'):
    '''decorated functions should NEVER change column `tokens`, redirect the authorized to `restricted_view`, invoking `check_cookie`'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            '''update token or set invalid token to ``'''
            admin = check_cookie(request)
            if admin:
                response = make_response(redirect(restricted_view))
                response.set_cookie('token', admin.token, max_age=604800, secure=True)
            else:
                response = func(*args, **kw)
                response.set_cookie('token', '', max_age=604800, secure=True)
            return response
        return wrapper
    return decorator

# @fun_logger('login')
def load_token(update_token=True, error_status_code=1):
    '''decorated functions should NEVER change column `tokens` and have <admin> as first argument,
    update token by default, return msg and error_status_code at /status'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            '''parser `token` from request, return immediately for invalid token or invoke decorated function'''
            parser = reqparse.RequestParser()
            parser.add_argument('token', type=str)
            # logging.info(parser.parse_args())
            admin = get_arg(parser.parse_args()['token'], None, check_token)
            if admin:
                if update_token:
                    admin.token = generate_random_string(32)
                    db.session.commit()
                response_dict = func(admin, *args, **kw)
                response_dict['token'] = admin.token
            else:
                response_dict = {'status': error_status_code, 'data': {'msg': '鉴权失败'}}
            return response_dict
        return wrapper
    return decorator
