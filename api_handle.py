#!/usr/env/python3
# -*- coding: UTF-8 -*-

from auth_handle import authenticate
from flask_restful import Resource, Api, reqparse
from mess import fun_logger, generate_random_string
from restful_handle import parse_all_args
from sql_handle import item_to_dict, get_jobs, get_records, get_tokens, get_volunteers, check_NoResultFound
from tables import db, Record
import json
import logging

api = Api()

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
