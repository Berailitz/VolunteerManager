#!/usr/env/python3
# -*- coding: UTF-8 -*-

import datetime
import functools
import logging
from flask import redirect, request, make_response
from flask_bcrypt import Bcrypt
from .mess import fun_logger, generate_random_string
from .sql_handle import get_tokens, check_NoResultFound
from .tables import db

bcrypt = Bcrypt()
def check_token(token):
    try:
        admin = get_tokens({'token': token, 'query_type': 'one'}, ['token'])
        logging.info('%r: token: %r.', admin, token)
        if datetime.datetime.now() > admin.login_time + datetime.timedelta(days=7):
            admin.token = ''
            return None
        else:
            return admin
    except Exception as e:
        if not check_NoResultFound(e, {'token': token, 'query_type': 'one'}):
            logging.exception(e)
            raise e
        return None

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
        return None

def authenticate(**credential):
    '''check credential and return user or None'''
    if credential['token']:
        return check_token(credential['token'])
    elif credential['username'] and credential['password']:
        return check_password(credential['username'], credential['password'])
    else:
        return None

def get_current_user(**credential):
    '''check credential and return current user with new token'''
    admin = authenticate(**credential)
    if admin:
        admin.token = generate_random_string(64)
        db.session.commit()
        return admin
    else:
        return None

def check_cookie(request):
    '''check cookie of request and return current user with new token'''
    try:
        current_token = request.cookies.get('token')
        current_user = get_current_user(token=current_token)
        if current_user:
            return current_user
        else:
            return None
    except KeyError as key_error:
        logging.info(key_error)
        return None

@fun_logger('login')
def admin_only(public_view='/'):
    '''decorated functions should NEVER change table `tokens`'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
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

@fun_logger('login')
def guest_only(restricted_view='/record'):
    '''decorated functions should NEVER change table `tokens`'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
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
