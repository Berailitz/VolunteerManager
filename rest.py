#!/usr/env/python3
# -*- coding: UTF-8 -*-

import datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy, orm
from flask_bcrypt import Bcrypt
import functools
import hashlib
import json
import logging
import random
import string
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://xh:xh@localhost/xh?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)

def fun_logger(text='Fun_logger'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            logging.info('%s:Called %s(%r, %r):', text, func.__name__, args, kw)
            result = func(*args, **kw)
            logging.info('%s:Returned %r:', text, result)
            return result
        return wrapper
    return decorator

def setLogging(LogPath):
    logging.basicConfig(level=logging.INFO,
        format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s',
        datefmt='%Y %b %d %H:%M:%S',
        filename=LogPath,
        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("Start ....")

class Token(db.Model):
    '''token table'''
    __tablename__ = 'tokens'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(64))
    token = db.Column(db.String(64))
    login_time = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    blank1 = db.Column(db.Integer)

    def __repr__(self):
        return '<Token %r>' % self.username

class Job(db.Model):
    '''job table'''
    __tablename__ = 'jobs'
    project_id = db.Column(db.Integer)
    project_name = db.Column(db.String(20))
    job_id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(30))
    job_start = db.Column(db.Date)
    job_end = db.Column(db.Date)
    director = db.Column(db.String(20))
    location = db.Column(db.String(30))
    note = db.Column(db.String(100))
    blank1 = db.Column(db.Integer)

    def __repr__(self):
        return '<Job %r@%r>' % (self.job_name, self.project_name)

class Record(db.Model):
    '''record table'''
    __tablename__ = 'records'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    job_date = db.Column(db.Date)
    working_time = db.Column(db.Integer)
    record_note = db.Column(db.String(40))
    operator_id = db.Column(db.Integer)
    operation_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    record_status = db.Column(db.Integer)

    def __init__(self, user_id, project_id, job_id, job_date, working_time, record_note, operator_id=0):
        self.user_id = user_id
        self.project_id = project_id
        self.job_id = job_id
        self.job_date = job_date
        self.working_time = working_time
        self.record_note = record_note
        self.operator_id = operator_id

    def __repr__(self):
        return '<Record %r>' % self.record_id

class Volunteer(db.Model):
    '''volunteer table'''
    __tablename__ = 'volunteers'
    user_id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer)
    username = db.Column(db.String(20))
    student_id = db.Column(db.String(20))
    class_index = db.Column(db.String(12))
    legal_name = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    age = db.Column(db.Integer)
    volunteer_time = db.Column(db.Float)
    note = db.Column(db.String(50))
    def __repr__(self):
        return '<Volunteer %r>' % self.legal_name

def parse_all_args(parser):
    parser.add_argument('job_id', type=int)
    parser.add_argument('legal_name', type=str)
    parser.add_argument('length', type=int)
    parser.add_argument('page', type=int)
    parser.add_argument('project_id', type=int)
    parser.add_argument('project_name', type=str)
    parser.add_argument('query_type', type=str)
    parser.add_argument('student_id', type=str)
    parser.add_argument('query_type', type=str)
    parser.add_argument('user_id', type=int)
    return parser.parse_args()

def get_arg(current, default):
    if current:
        return current
    else:
        return default

def item_to_dict(item, const_removed={}):
    item_dict = item.__dict__.copy()
    del item_dict['_sa_instance_state']
    for removed_attr in const_removed:
        del item_dict[removed_attr]
    for key in item_dict.keys():
        item_dict[key] = str(item_dict[key])
    return item_dict

# @fun_logger()
def query_items(table_object, valid_key_list, arg_dict, target_key_list=None):
    table_query = table_object.query
    if not target_key_list:
        target_key_list = arg_dict.keys()
    if not 'query_type' in arg_dict.keys():
        arg_dict['query_type'] = 'all'
    for (key, value) in arg_dict.items():
        if value and key in valid_key_list:
            table_query = table_query.filter(getattr(table_object, key)==value)
            # logging.info(table_query.all())
    if arg_dict['query_type'] == 'one':
        return table_query.one()
    if arg_dict['query_type'] == 'page':
        return table_query.paginate(get_arg(arg_dict['page'], 1), get_arg(arg_dict['length'], 200), False).items
    if arg_dict['query_type'] == 'all':
        return table_query.all()
    if arg_dict['query_type'] == 'first':
        return table_query.first()

def get_volunteers(arg_dict, target_key_list=None):
    volunteer_keys = ['user_id', 'volunteer_id', 'username', 'student_id', 'legal_name', 'phone', 'email', 'gender', 'age', 'volunteer_time', 'note']
    return query_items(Volunteer, volunteer_keys, arg_dict, target_key_list)

def get_records(arg_dict, target_key_list=None):
    record_keys = ['record_id', 'user_id', 'project_id', 'job_id', 'job_date', 'working_time', 'record_note', 'operator_id', 'operation_date', 'record_status']
    return query_items(Record, record_keys, arg_dict, target_key_list)

def get_jobs(arg_dict, target_key_list=None):
    job_keys = ['project_id', 'project_name', 'job_id', 'job_name', 'job_start', 'job_end', 'director', 'location', 'note']
    return query_items(Job, job_keys, arg_dict, target_key_list)

def get_tokens(arg_dict, target_key_list=None):
    token_keys = ['admin_id', 'username', 'password', 'token', 'login_time']
    return query_items(Token, token_keys, arg_dict, target_key_list)

def check_NoResultFound(e, args=None):
    if isinstance(e, orm.exc.NoResultFound):
        logging.info(str(e) + ' @ ' + str(args))
        return True
    else:
        return False

generate_random_string = lambda length: ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

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

class token_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        # login_time = time.strftime('%Y-%m-%d %H:%M:%S',)
        admin = authenticate(**args)
        if admin:
            admin.token = generate_random_string(64)
            db.session.commit()
            return {'status': 0, 'data': {'token': admin.token}}
        else:
            return {'status': 1}

class volunteer_api(Resource):
    def get(self):
        args = parse_all_args(reqparse.RequestParser())
        try:
            the_volunteer = get_volunteers(args)
        except Exception as e:
            if not check_NoResultFound(e, args):
                logging.exception(e)
                raise e
            return {'status': 1, 'data': {'info': {}, 'msg': '查无此人', 'records': []}}
        volunteer_dict = item_to_dict(the_volunteer, set())
        # logging.info((length * page_index, length * (page_index + 1)))
        return {'status': 0, 'data': {'info': volunteer_dict}}

class job_api(Resource):
    def get(self):
        args = parse_all_args(reqparse.RequestParser())
        try:
            job_all = get_jobs(args)
        except Exception as e:
            if not check_NoResultFound(e, args):
                logging.exception(e)
                raise e
        job_list = list(map(lambda job_item: job_item.job_name, job_all))
        return {'data': job_list}

class record_api(Resource):
    def get(self):
        args = parse_all_args(reqparse.RequestParser())
        record_all = get_records(args)
        if not type(record_all) == list:
            record_all = [record_all]
        for record_index in range(len(record_all)):
            # logging.info(record_list[record_index])
            try:
                operator_name = get_volunteers({'user_id': record_all[record_index].operator_id, 'query_type': 'one'}, ['user_id']).legal_name
                record_all[record_index].operator_name = operator_name
            except Exception as e:
                if not check_NoResultFound(e, args):
                    logging.exception(e)
                    raise e
        record_list = list(map(item_to_dict, record_all, [set()] * len(record_all)))
        logging.info(record_list)
        return {'data': {'records': record_list}}
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        raw_args = parser.parse_args()
        logging.info(raw_args)
        args = json.loads(raw_args['data'])
        args['query_type'] = 'one'
        try:
            the_vol = get_volunteers(args, ['student_id', 'legal_name'])
        except Exception as e:
            if not check_NoResultFound(e, args):
                logging.exception(e)
                raise e
            return {'status': 1, 'data': {'msg': '查无此人'}}
        try:
            the_job = get_jobs(args)
        except Exception as e:
            if not check_NoResultFound(e, args):
                logging.exception(e)
                raise e
            return {'status': 1, 'data': {'msg': '查无此项目'}}
        new_rec = Record(the_vol.user_id, the_job.project_id, the_job.job_id, args['job_date'], args['working_time'], args['record_note'])
        new_rec.operator_id = the_vol.user_id
        db.session.add(new_rec)
        db.session.commit()
        return {'status': 0, 'data': {'msg': '已录入'}}

class relationship_api(Resource):
    def get(self):
        project_id_dict = dict()
        project_name_dict = dict()
        projects_id_2_name = dict(set(map(lambda pro: (pro.project_id, pro.project_name), get_jobs({'query_type': 'all'}))))
        for single_project_id in projects_id_2_name.keys():
            distinct_jobs = dict(set(map(lambda job: (job.job_id, job.job_name),
                get_jobs({'project_name': projects_id_2_name[single_project_id], 'query_type': 'all'}))))
            project_id_dict[single_project_id] = {
                'project_name': projects_id_2_name[single_project_id],
                'job_id_dict': dict((single_job_id, distinct_jobs[single_job_id]) for single_job_id in distinct_jobs.keys()),
                'job_name_dict': dict((distinct_jobs[single_job_id], single_job_id) for single_job_id in distinct_jobs.keys())
            }
            project_name_dict[projects_id_2_name[single_project_id]] = single_project_id
        return {'status': 0, 'data': {'project_id_dict': project_id_dict, 'project_name_dict': project_name_dict}}

api.add_resource(token_api, '/tokens')
api.add_resource(volunteer_api, '/volunteers')
api.add_resource(job_api, '/jobs')
api.add_resource(record_api, '/records')
api.add_resource(relationship_api, '/relationship')

if __name__ == '__main__':
    setLogging('log.txt')
    app.run(debug=True)
