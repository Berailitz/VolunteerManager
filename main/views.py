#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template

def create_main_blueprint():
    main_blueprint = Blueprint('main', __name__, template_folder='templates')
    main_blueprint.add_url_rule('/', 'index', show_index_page)
    main_blueprint.add_url_rule('/project', 'project', show_project_page)
    main_blueprint.add_url_rule('/record', 'record', show_record_page)
    main_blueprint.add_url_rule('/volunteer', 'volunteer', show_volunteer_page)
    return main_blueprint

def show_index_page():
    return render_template('index.html')

def show_project_page():
    return render_template('project.html')

def show_record_page():
    return render_template('record.html')

def show_volunteer_page():
    return render_template('volunteer.html')
