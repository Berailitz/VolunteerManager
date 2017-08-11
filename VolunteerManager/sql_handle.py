"""communicate with sql tables"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
import os
import os.path as path
import time
import pandas
import sqlalchemy
from sqlalchemy import create_engine
from .config import AppConfig
from .mess import generate_random_string, fun_logger
from .restful_helper import get_arg
from .tables import Token, Job, Record, Volunteer

engine = create_engine(AppConfig.SQLALCHEMY_DATABASE_URI)

def item_to_dict(item, const_removed={}):
    """transfer sqlalchemy object to a serializable dict, with all value transfered to `string`,
    remove columns in set `const_removed`"""
    item_dict = item.__dict__.copy()
    del item_dict['_sa_instance_state']
    for removed_attr in const_removed:
        del item_dict[removed_attr]
    for key in item_dict.keys():
        item_dict[key] = str(item_dict[key])
    return item_dict

# @fun_logger()
def query_items(table_object, valid_key_list, arg_dict, target_key_list=None):
    """PRIVATE: Query items in `table_object`, with args in `arg_dict`, whose keys should be in both
    `valid_key_list` and non-None `target_key_list`, when `target_key_list` is set to None, all keys
    in `valid_key_list` will be queried."""
    query_object = table_object.query
    if not target_key_list:
        target_key_list = arg_dict.keys()
    for (key, value) in arg_dict.items():
        if value and key in valid_key_list and key in target_key_list:
            query_object = query_object.filter(getattr(table_object, key) == value)
            # logging.info(query_object.all())
    return query_object

def select_type(query_result, arg_dict, query_type):
    """return query_result.query_type() or query_result.paginate(...) accordingly. A list (which can be empty)
    is returned with `query_type` of `page` and `all`, an item otherwise. With `query_type` `one`, error
    `sqlalchemy.orm.exc.NoResultFound` and `sqlalchemy.orm.exc.MultipleResultsFound` may be raised accordingly.
     Be CAUTIOUS wih `query_type`, when a list/page of up to 200 items is returned (by default)."""
    MAX_ITEMS_COUNT_PER_PAGE = AppConfig.MAX_ITEMS_COUNT_PER_PAGE
    if query_type in ['one', 'all', 'first']:
        return getattr(query_result, query_type)()
    elif query_type == 'page':
        return query_result.paginate(get_arg(arg_dict['page'], 1), get_arg(arg_dict['length'], MAX_ITEMS_COUNT_PER_PAGE), False).items
    else:
        raise ValueError(f'Invalid query_type: {query_type}')

def get_volunteers(arg_dict, query_type='all', target_key_list=None):
    """get volunteer object(s)"""
    volunteer_keys = ['user_id', 'volunteer_id', 'username', 'student_id', 'legal_name', 'phone']
    volunteer_keys += ['email', 'gender', 'age', 'volunteer_time', 'note']
    query_object = query_items(Volunteer, volunteer_keys, arg_dict, target_key_list)
    return select_type(query_object, arg_dict, query_type)

def get_records(arg_dict, query_type='all', target_key_list=None, const_status_type_list=[1]):
    """get record object(s) with `record_status` of `1` by default"""
    record_keys = ['record_id', 'user_id', 'project_id', 'job_id', 'working_date', 'working_time', 'record_note']
    record_keys += ['operator_id', 'operation_time', 'record_status']
    query_object = query_items(Record, record_keys, arg_dict, target_key_list)
    query_object = query_object.filter(Record.record_status.in_(const_status_type_list))
    return select_type(query_object, arg_dict, query_type)

def get_jobs(arg_dict, query_type='all', target_key_list=None):
    """get job object(s)"""
    job_keys = ['project_id', 'project_name', 'job_id', 'job_name', 'job_start', 'job_end', 'director', 'location', 'note']
    query_object = query_items(Job, job_keys, arg_dict, target_key_list)
    return select_type(query_object, arg_dict, query_type)

def get_tokens(arg_dict, query_type='all', target_key_list=None):
    """get token object(s)"""
    token_keys = ['admin_id', 'username', 'password', 'token', 'login_time']
    query_object = query_items(Token, token_keys, arg_dict, target_key_list)
    return select_type(query_object, arg_dict, query_type)

def export_to_excel(export_type, folder_path=AppConfig.DOWNLOAD_PATH, create_folder=True):
    """export sql table to disk at relative path `folder_path`, which may be recursively created
    if `create_folder` is True (Default)"""
    if export_type == 'all_in_one':
        data_frame = pandas.read_sql_query(AppConfig.ALL_IN_ONE_SQL_QUERY_COMMAND, engine)
    else:
        data_frame = pandas.read_sql_table(export_type, engine)
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    module_dir = path.split(path.realpath(__file__))[0]
    filename = '%s_%s_%s.xlsx' % (export_type, current_time, generate_random_string(6))
    real_folder = path.join(module_dir, folder_path)
    if create_folder:
        os.makedirs(real_folder, exist_ok=True)
    real_path = path.join(real_folder, filename)
    data_frame.to_excel(real_path, sheet_name=export_type)
    return filename

def export_to_json(table_name, folder_path=AppConfig.BACKUP_FOLDER, create_folder=True):
    """backup sql table to json file at relative path `folder_path`, which may be recursively created
    if `create_folder` is True (Default)"""
    logging.info(f'Backup of table {table_name} to json file start')
    data_frame = pandas.read_sql_table(table_name, engine)
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    module_dir = path.split(path.realpath(__file__))[0]
    filename = '%s_%s_%s.xlsx' % (table_name, current_time, generate_random_string(6))
    real_folder = path.join(module_dir, folder_path)
    if create_folder:
        os.makedirs(real_folder, exist_ok=True)
    real_path = path.join(real_folder, filename)
    data_frame.to_excel(real_path, sheet_name=table_name)
    logging.info(f'Backup completed @ {real_path}')
    return filename

def import_volunteers(data_list):
    """import `data_list` to sql table `temp`, which will be TRUNCATED to avoid conflict while
    being `appended` with new rows. These rows will be merged into table `volunteers` later."""
    data_frame = pandas.DataFrame(data_list)
    logging.info('Truncate temp table `volunteers_temp`')
    engine.execute(AppConfig.SYNC_TRUNCATE_TEMP_TABLE_COMMAND)
    column_type = {
        'user_id': sqlalchemy.types.Integer,
        'volunteer_id': sqlalchemy.types.String(20),
        'username': sqlalchemy.types.String(20),
        'student_id': sqlalchemy.types.String(20),
        'class_index': sqlalchemy.types.String(12),
        'legal_name': sqlalchemy.types.String(40),
        'phone': sqlalchemy.types.String(20),
        'email': sqlalchemy.types.String(50),
        'gender': sqlalchemy.types.String(1),
        'age': sqlalchemy.types.Integer,
        'volunteer_time': sqlalchemy.types.Float,
        'note': sqlalchemy.types.String(50)
    }
    logging.info('Insert data to temp table `volunteers_temp`')
    data_frame.to_sql('temp', engine, if_exists='append', index=False, chunksize=100, dtype=column_type)
    logging.info('Merge data to main table `volunteers`')
    engine.execute(AppConfig.SYNC_VOLUNTEER_SQL_COMMAND)
    logging.info('Truncate temp table `volunteers_temp`')
    engine.execute(AppConfig.SYNC_TRUNCATE_TEMP_TABLE_COMMAND)
