#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Blueprint, make_response, render_template
from ..auth_handle import admin_only, guest_only
from ..mess import fun_logger

def create_main_blueprint():
    main_blueprint = Blueprint('main', __name__, template_folder='templates')
    main_blueprint.add_url_rule('/', 'index', show_index_page)
    main_blueprint.add_url_rule('/project', 'project', show_project_page)
    main_blueprint.add_url_rule('/record', 'record', show_record_page)
    main_blueprint.add_url_rule('/volunteer', 'volunteer', show_volunteer_page)
    return main_blueprint

@fun_logger('login')
@guest_only()
def show_index_page():
    return make_response(render_template('index.html', page_url='/index', page_title='登录'))

@admin_only()
@fun_logger('login')
def show_project_page():
    return make_response(render_template('project.html', page_url='/project', page_title='志愿项目管理'))

@admin_only()
def show_record_page():
    return make_response(render_template('record.html', page_url='/record', page_title='志愿时长录入'))

@admin_only()
def show_volunteer_page():
    return make_response(render_template('volunteer.html', page_url='/volunteer', page_title='志愿者信息查询'))

@admin_only()
def show_download_page():
    return make_response(render_template('download.html', page_url='/download', page_title='表格下载'))
