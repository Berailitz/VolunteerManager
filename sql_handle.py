#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask_sqlalchemy import orm
from .restful_helper import get_arg
from .tables import Token, Job, Record, Volunteer
import logging

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
