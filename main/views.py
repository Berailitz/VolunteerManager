#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import render_template
from . import main_blueprint

@main_blueprint.route('/')
@main_blueprint.route('/index')
def show_index_page():
    return render_template('index.html')

@main_blueprint.route('/project')
def show_project_page():
    return render_template('project.html')

@main_blueprint.route('/record')
def show_record_page():
    return render_template('record.html')

@main_blueprint.route('/volunteer')
def show_volunteer_page():
    return render_template('volunteer.html')
