"""define all tables"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Token(db.Model):
    """token table"""
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
    """job table"""
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
    """record table"""
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
    record_status = db.Column(db.Integer, server_default=1)

    def __init__(self, user_id=0, project_id=0, job_id=0, job_date='', working_time=0, record_note='', operator_id=0):
        """initialize a record object, default values may be invalid"""
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
    """volunteer table"""
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
