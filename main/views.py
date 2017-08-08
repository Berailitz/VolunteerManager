#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from ..auth_handle import admin_only, guest_only

def create_main_blueprint():
    main_blueprint = Blueprint('main', __name__, template_folder='templates')
    main_blueprint.add_url_rule('/', 'index', show_index_page)
    main_blueprint.add_url_rule('/project', 'project', show_project_page)
    main_blueprint.add_url_rule('/record', 'record', show_record_page)
    main_blueprint.add_url_rule('/volunteer', 'volunteer', show_volunteer_page)
    return main_blueprint

@guest_only
def show_index_page():
    return render_template('index.html')

@admin_only
def show_project_page():
    return render_template('project.html')

@admin_only
def show_record_page():
    return render_template('record.html')

@admin_only
def show_volunteer_page():
    return render_template('volunteer.html')
