"""import json to sql"""
#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import time
import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker

ROW_BASE = declarative_base()

def set_logger(log_file_path):
    """set logger"""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s',
        datefmt='%Y %b %d %H:%M:%S',
        filename=log_file_path,
        filemode='a'
        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("Start ....")

class Connector(object):
    """communicate with sql"""
    def __init__(self, url, ifecho=False):
        self.engine = create_engine(url, echo=ifecho)
        self.session = None

    def __enter__(self):
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()
        logging.info("Connected.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.session.rollback()
            logging.exception(exc_type)
            logging.error("exc_value: " + str(exc_value) + "\n" + str(traceback))
        self.session.close()
        logging.info("Rollbacked and disconnected.")

    def import_json(self, json_file_path="volunteer_list_int.json", interval=0.01):
        """import volunteers from json file to sql"""
        with open(json_file_path, "r") as json_file:
            volunteer_list = json.load(json_file)
        logging.info("Scanning volunteers from json file: " + str(len(volunteer_list)))
        keys = ['user_id', 'volunteer_id', 'username', 'student_id', 'legal_name', 'phone']
        keys = keys + ['email', 'gender', 'age', 'volunteer_time', 'note', 'blank2']
        # input("Press Enter to start...")
        for vol in volunteer_list:
            self.session.add(Volunteer(**dict(zip(keys, vol + ['', '']))))
            self.session.commit()
            logging.info("Adding " + str(vol))
            time.sleep(interval)
        self.session.close()
        print('Import from json file finished')

    def query_volunteers(self):
        """query for volunteers"""
        return self.session.query(Volunteer)

if __name__ == '__main__':
    set_logger("log.txt")
    with Connector('mysql+pymysql://xh:xh@localhost/xh?charset=utf8', ifecho=True) as my_connector:
        print(my_connector.query_volunteers().filter(Volunteer.user_id == 17270).all())



def transfer_to_sql(table, column_name, query_value):
    return (getattr(table, column_name) == query_value, )


#!/usr/env/python3
# -*- coding: UTF-8 -*-
import json
from flask import Flask
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
    """record object"""
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
        return '<Job %r@%r>' % (self.job_name, project_name)

class Record(db.Model):
    """record object"""
    __tablename__ = 'records'
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    job_date = db.Column(db.Date)
    working_time = db.Column(db.Integer)
    record_note = db.Column(db.String(40))
    operator_id = db.Column(db.Integer)
    operation_date = db.Column(db.Date)
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
    """vlounteer object"""
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
        args = parser.parse_args()
        length = get_arg(args['length'], 20)
        page_index = get_arg(args['page'], 1) - 1
        # length = int(request.args.get('length', ''))
        volunteer_all = Volunteer.query.all()
        volunteer_list = list(map(item_to_json, volunteer_all, [set(['blank2'])] * len(volunteer_all)))
        print((length * page_index, length * (page_index + 1)))
        return {'data': volunteer_list[length * page_index:length * (page_index + 1)]}

class job_api(Resource):
    def get(self):
        print(request.args)
        parser = reqparse.RequestParser()
        parser.add_argument('length', type=int)
        parser.add_argument('page', type=int)
        args = parser.parse_args()
        length = get_arg(args['length'], 100)
        page_index = get_arg(args['page'], 1) - 1
        # length = int(request.args.get('length', ''))
        job_all = Job.query.all()
        job_list = list(map(item_to_json, job_all, [set(['blank2'])] * len(job_all)))
        print((length * page_index, length * (page_index + 1)))
        return {'data': job_list[length * page_index:length * (page_index + 1)]}

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
        print(request.args)
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        raw_args = parser.parse_args()
        args = json.loads(raw_args['data'])
        # login_json = json.loads(args['secret'].replace('\'', '\"'))
        the_vol = Volunteer.query.filter(Volunteer.student_id==args['student_id']).filter(Volunteer.legal_name==args['legal_name']).all()
        the_job = Job.query.filter(Job.job_id==args['job_id']).filter(Job.project_id==args['project_id']).all()
        if not len(the_vol) == 1:
            return {'status': 1, 'data': {'msg': '查无此人'}}
        elif len(the_job) == 1:
            return {'status': 1, 'data': {'msg': '查无此项目'}}
        new_rec = Record(the_vol.user_id, the_job.project_id, the_job.job_id, args['job_date'], args['working_time'], args['record_note'])
        Record.add(new_rec)
        return {'status': 0, 'data': {'msg': '已录入'}}


api.add_resource(volunteer_api, '/volunteers')
api.add_resource(job_api, '/jobs')
api.add_resource(record_api, '/records')

if __name__ == '__main__':
    app.run(debug=True)