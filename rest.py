#!/usr/env/python3
# -*- coding: UTF-8 -*-
import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://xh:xh@localhost/xh?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG']=True
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
db = SQLAlchemy(app)
api = Api(app)

class Job(db.Model):
    '''job object'''
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
    '''record object'''
    __tablename__ = 'records'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    job_date = db.Column(db.Date)
    working_time = db.Column(db.Integer)
    record_note = db.Column(db.String(40))
    operator_id = db.Column(db.Integer)
    operation_date = db.Column(db.Date, server_default=db.func.current_timestamp())
    blank1 = db.Column(db.Integer)

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

rec = Record

class Volunteer(db.Model):
    '''vlounteer object'''
    __tablename__ = 'volunteers'
    user_id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer)
    username = db.Column(db.String(20))
    student_id = db.Column(db.String(20))
    legal_name = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    age = db.Column(db.Integer)
    volunteer_time = db.Column(db.Float)
    note = db.Column(db.String(50))
    blank2 = db.Column(db.Integer)
    def __repr__(self):
        return '<Volunteer %r>' % self.legal_name

vol = Volunteer
vol_all = vol.query.all()

def get_arg(current, default):
    if current:
        return current
    else:
        return default

def item_to_json(item, removed=set()):
    item_dict = item.__dict__.copy()
    del item_dict['_sa_instance_state']
    for removed_attr in removed:
        del item_dict[removed_attr]
    return json.dumps(item_dict, ensure_ascii=False)

class volunteer_api(Resource):
    def get(self):
        print(request.args)
        parser = reqparse.RequestParser()
        parser.add_argument('length', type=int)
        parser.add_argument('page', type=int)
        parser.add_argument('student_id', type=str)
        parser.add_argument('legal_name', type=str)
        args = parser.parse_args()
        student_id = get_arg(args['student_id'], '')
        legal_name = get_arg(args['legal_name'], '')
        length = get_arg(args['length'], 20)
        page_index = get_arg(args['page'], 1) - 1
        # length = int(request.args.get('length', ''))
        volunteer_all = Volunteer.query.filter(Volunteer.student_id==student_id).filter(Volunteer.legal_name==legal_name).all()
        volunteer_list = list(map(item_to_json, volunteer_all, [set(['blank2'])] * len(volunteer_all)))
        print((length * page_index, length * (page_index + 1)))
        return {'data': volunteer_list[length * page_index:length * (page_index + 1)]}

class job_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('length', type=int)
        # parser.add_argument('page', type=int)
        parser.add_argument('project_name', type=str)
        args = parser.parse_args()
        # length = get_arg(args['length'], 20)
        # page_index = get_arg(args['page'], 1) - 1
        # length = int(request.args.get('length', ''))
        print(args)
        job_all = Job.query.filter(Job.project_name==args['project_name']).all()
        job_list = list(map(lambda job_item: job_item.job_name, job_all))
        return {'data': job_list}

class project_api(Resource):
    def get(self):
        # print(request.args)
        # parser = reqparse.RequestParser()
        # parser.add_argument('length', type=int)
        # parser.add_argument('page', type=int)
        # args = parser.parse_args()
        # length = get_arg(args['length'], 100)
        # page_index = get_arg(args['page'], 1) - 1
        # length = int(request.args.get('length', ''))
        project_all = Job.query.order_by(Job.project_name).all()
        distinct_list = list(set(map(lambda pro: pro.project_name, project_all)))
        print(distinct_list)
        return {'data': distinct_list}

class record_api(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('length', type=int)
        parser.add_argument('page', type=int)
        args = parser.parse_args()
        length = get_arg(args['length'], 20)
        page_index = get_arg(args['page'], 1) - 1
        # length = int(request.args.get('length', ''))
        record_all = Record.query.all()
        record_list = list(map(item_to_json, record_all, [set(['blank1'])] * len(record_all)))
        return {'data': record_list[length * page_index:length * (page_index + 1)]}
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        raw_args = parser.parse_args()
        print(raw_args)
        args = json.loads(raw_args['data'])
        # login_json = json.loads(args['secret'].replace('\'', '\"'))
        # vol_list = Volunteer.query.filter(Volunteer.student_id==args['student_id']).filter(Volunteer.legal_name==args['legal_name']).all()
        # job_list = Job.query.filter(Job.job_name==args['job_name']).filter(Job.project_name==args['project_name']).all()
        # # print(Job.query.all()[0].job_name==args['job_name'])
        # # print(Job.query.all()[0].project_name==args['project_name'])
        # print(the_job)
        # print(len(the_job))
        try:
            the_vol = Volunteer.query.filter(Volunteer.student_id==args['student_id']).filter(Volunteer.legal_name==args['legal_name']).one()
        except Exception as e:
            return {'status': 1, 'data': {'msg': '查无此人'}}
        try:
            the_job = Job.query.filter(Job.project_name==args['project_name']).filter(Job.job_name==args['job_name']).one()
        except Exception as e:
            return {'status': 1, 'data': {'msg': '查无此项目'}}
        # if len(vol_list) != 1:
        #     return {'status': 1, 'data': {'msg': '查无此人'}}
        # elif len(job_list) != 1:
        #     return {'status': 1, 'data': {'msg': '查无此项目'}}
        new_rec = Record(the_vol.user_id, the_job.project_id, the_job.job_id, args['job_date'], args['working_time'], args['record_note'])
        new_rec.operator_id = the_vol.user_id
        # new_rec.operation_date = None
        print(new_rec)
        db.session.add(new_rec)
        db.session.commit()
        return {'status': 0, 'data': {'msg': '已录入'}}

api.add_resource(volunteer_api, '/volunteers')
api.add_resource(job_api, '/jobs')
api.add_resource(project_api, '/projects')
api.add_resource(record_api, '/records')

if __name__ == '__main__':
    app.run(debug=True)
