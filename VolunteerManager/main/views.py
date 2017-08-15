"""main views and blueprint"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

from flask import Blueprint, make_response, render_template, request
from ..auth_handle import admin_only_view, guest_only_view
from ..mess import fun_logger

def create_main_blueprint():
    """create and return main blueprint, which should be registered later"""
    main_blueprint = Blueprint('main', __name__, template_folder='templates')
    main_blueprint.add_url_rule('/', 'index', show_index_page)
    main_blueprint.add_url_rule('/project', 'project', show_project_page)
    main_blueprint.add_url_rule('/record', 'record', show_record_page)
    main_blueprint.add_url_rule('/volunteer', 'volunteer', show_volunteer_page)
    main_blueprint.add_url_rule('/edit', 'edit', show_edit_page)
    main_blueprint.add_url_rule('/download', 'download', show_download_page)
    main_blueprint.add_url_rule('/advanced', 'advanced', show_advanced_page)
    return main_blueprint

def render_with_pjax(template_name, **kwargs):
    """DEBUG: enable pjax for templates"""
    is_pjax = "X-PJAX" in request.headers
    return render_template(template_name, is_pjax=is_pjax, **kwargs)

@guest_only_view()
def show_index_page():
    return make_response(render_with_pjax('index.html', page_url='/index', page_title='登录'))

@admin_only_view()
def show_project_page():
    return make_response(render_with_pjax('project.html', page_url='/project', page_title='志愿项目管理'))

@admin_only_view()
def show_record_page():
    return make_response(render_with_pjax('record.html', page_url='/record', page_title='志愿时长录入'))

@admin_only_view()
def show_volunteer_page():
    return make_response(render_with_pjax('volunteer.html', page_url='/volunteer', page_title='志愿者信息查询'))

@admin_only_view()
def show_edit_page():
    return make_response(render_with_pjax('edit.html', page_url='/edit', page_title='时长记录编辑'))

@admin_only_view()
def show_download_page():
    return make_response(render_with_pjax('download.html', page_url='/download', page_title='记录表格下载'))

@admin_only_view()
def show_advanced_page():
    return make_response(render_with_pjax('advanced.html', page_url='/advanced', page_title='高级功能'))
