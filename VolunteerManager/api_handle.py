'''define all apis under /api/'''
#!/usr/env/python3
# -*- coding: UTF-8 -*-

import json
import logging
import os
import os.path as path
import shutil
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import orm
from .auth_handle import get_current_user, load_token
from .config import AppConfig
from .mess import fun_logger
from .restful_helper import parse_all_args
from .sql_handle import export_to_excel, item_to_dict, get_jobs, get_records, get_tokens, get_volunteers
from .tables import db, Record

def create_api():
    '''return api object at startup'''
    api = Api()
    api.add_resource(TokenApi, '/api/tokens')
    api.add_resource(VolunteerApi, '/api/volunteers')
    api.add_resource(JobApi, '/api/jobs')
    api.add_resource(RecordApi, '/api/records')
    api.add_resource(RelationshipApi, '/api/relationship')
    api.add_resource(ExcelApi, '/api/download')
    return api

class TokenApi(Resource):
    '''handle /api/tokens'''
    def get(self):
        '''GET method, get token with password or new token by get_current_user'''
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        # login_time = time.strftime('%Y-%m-%d %H:%M:%S',)
        admin = get_current_user(**args)
        if admin:
            return {'status': 0, 'token': admin.token}
        else:
            return {'status': 1, 'data': {'msg': '鉴权失败'}}

class VolunteerApi(Resource):
    '''handle /api/volunteers'''
    @load_token()
    def get(admin, self):
        '''GET method, get volunteer info, ONE per call, return dict at /data/info'''
        args = parse_all_args(reqparse.RequestParser())
        try:
            the_volunteer = get_volunteers(args)
        except orm.exc.NoResultFound as identifier:
            logging.warning('%r', identifier)
            return {'status': 1, 'data': {'info': {}, 'msg': '查无此人'}}
        volunteer_dict = item_to_dict(the_volunteer, set())
        # logging.info((length * page_index, length * (page_index + 1)))
        return {'status': 0, 'data': {'info': volunteer_dict}}

class JobApi(Resource):
    '''handle /api/jobs'''
    @load_token()
    def get(admin, self):
        '''GET method，return job list at /data'''
        args = parse_all_args(reqparse.RequestParser())
        try:
            job_all = get_jobs(args)
        except orm.exc.NoResultFound as identifier:
            logging.warning('%r', identifier)
            return {'status': 1, 'data': {'info': {}, 'msg': '查无此项'}}
        job_list = list(map(lambda job_item: job_item.job_name, job_all))
        return {'status': 0, 'data': job_list}

class RecordApi(Resource):
    '''handle /api/records'''
    @load_token()
    def get(admin, self):
        '''GET method, return record list at /data/records'''
        args = parse_all_args(reqparse.RequestParser())
        try:
            record_all = get_records(args)
        except orm.exc.NoResultFound as identifier:
            logging.warning('%r', identifier)
            return {'status': 1, 'data': {'msg': '查无此记录'}}
        if not isinstance(record_all, list):
            record_all = [record_all]
        for record_index in range(len(record_all)):
            # logging.info(record_list[record_index])
            try:
                operator = get_tokens({'admin_id': record_all[record_index].operator_id, 'query_type': 'one'}, ['admin_id'])
                operator_name = operator.username
                record_all[record_index].operator_name = operator_name
                volunteer = get_volunteers({'user_id': record_all[record_index].user_id, 'query_type': 'one'}, ['user_id'])
                legal_name = volunteer.legal_name
                record_all[record_index].legal_name = legal_name
                student_id = volunteer.student_id
                record_all[record_index].student_id = student_id
            except orm.exc.NoResultFound as identifier:
                logging.warning('%r', identifier)
        record_list = list(map(item_to_dict, record_all, [set()] * len(record_all)))
        logging.info(record_list)
        return {'data': {'records': record_list}}

    @load_token(False)
    def post(admin, self):
        '''POST method, return msg at /data/msg'''
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        raw_args = parser.parse_args()
        logging.info(raw_args)
        args = json.loads(raw_args['data'])
        args['query_type'] = 'one'
        # logging.info(args)
        try:
            the_rec = get_records({'record_id': int(args['record_id']), 'query_type': 'one'})
        except orm.exc.NoResultFound as identifier:
            logging.warning('%r', identifier)
            return {'status': 1, 'data': {'msg': '查无此记录'}}
        try:
            if 'student_id' in args and args['student_id']:
                the_vol = get_volunteers(args)
                the_rec.user_id = the_vol.user_id
            if 'job_id' in args and args['job_id']:
                the_job = get_jobs(args)
                the_rec.project_id = the_job.project_id
                the_rec.job_id = the_job.job_id
        except orm.exc.NoResultFound as identifier:
            logging.warning('%r', identifier)
            return {'status': 1, 'data': {'msg': '志愿项目或志愿者参数错误'}}
        for key in ['job_date', 'working_time', 'record_note']:
            if key in args and args[key]:
                setattr(the_rec, key, args[key])
        the_rec.operator_id = admin.admin_id
        db.session.commit()
        return {'status': 0, 'data': {'msg': f'已更新(ID:{the_rec.record_id})'}}

    @load_token(False)
    def put(admin, self):
        '''PUT method, return msg at /data/msg'''
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        raw_args = parser.parse_args()
        logging.info(raw_args)
        args = json.loads(raw_args['data'])
        args['query_type'] = 'one'
        try:
            the_vol = get_volunteers(args, ['student_id', 'legal_name'])
        except orm.exc.NoResultFound as identifier:
            logging.warning('%r', identifier)
            return {'status': 1, 'data': {'msg': '查无此人'}}
        try:
            the_job = get_jobs(args)
        except orm.exc.NoResultFound as identifier:
            logging.warning('%r', identifier)
            return {'status': 1, 'data': {'msg': '查无此项目'}}
        new_rec = Record(the_vol.user_id, the_job.project_id, the_job.job_id, args['job_date'], args['working_time'], args['record_note'])
        new_rec.operator_id = admin.admin_id
        db.session.add(new_rec)
        db.session.commit()
        return {'status': 0, 'data': {'msg': f'已录入(ID:{new_rec.record_id})'}}

class RelationshipApi(Resource):
    '''handle /api/relationship'''
    @load_token()
    def get(admin, self):
        '''GET method, return relationship dict at /data/, receive no argument but `token`'''
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

class ExcelApi(Resource):
    '''handle /api/download'''
    @load_token()
    def get(admin, self):
        '''GET method, return download url at /data/download_url, may take some time'''
        parser = reqparse.RequestParser()
        parser.add_argument('export_type', type=str)
        raw_args = parser.parse_args()
        export_type = raw_args['export_type']
        if export_type:
            try:
                filename = export_to_excel(export_type)
            except Exception as identifier:
                logging.exception('%r: %r', identifier, identifier.args)
                return {'status': 1, 'data': {'msg': '%r' % (identifier, )}}
            return {'status': 0, 'data': {'download_url': f'/static/temp/{filename}'}}
        else:
            return {'status': 1, 'data': {'msg': '参数错误'}}

    @load_token()
    def delete(admin, self):
        '''DELETE method, return msg at /data/msg'''
        module_dir = path.split(path.realpath(__file__))[0]
        download_folder = AppConfig.DOWNLOAD_PATH
        download_path = path.join(module_dir, download_folder)
        try:
            if path.exists(download_path):
                shutil.rmtree(download_path)
                os.mkdir(download_path)
            return {'status': 0}
        except Exception as identifier:
            logging.exception('%r: %r', identifier, identifier.args)
            return {'status': 1, 'data': {'msg': str(identifier)}}
