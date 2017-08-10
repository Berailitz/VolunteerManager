"""config of this app"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

class AppConfig(object):
    """config class"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xh:xh@localhost/xh?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = '67gyubinjmokl,pl'
    DOWNLOAD_PATH = 'main/static/temp'
    TOKEN_LENGTH = 32
    MAX_ITEMS_COUNT_PER_PAGE = 200
    ALL_IN_ONE_SQL_QUERY_COMMAND = "SELECT `record_id`, `records`.`user_id`, `project_name`, `job_name`, `job_date`, `working_time`,"
    ALL_IN_ONE_SQL_QUERY_COMMAND += " `record_note`, `operation_date`, `tokens`.`username`, `record_status`, `legal_name`, `student_id`"
    ALL_IN_ONE_SQL_QUERY_COMMAND += " FROM `records` LEFT JOIN `volunteers` ON `records`.`user_id` = `volunteers`.`user_id` LEFT JOIN "
    ALL_IN_ONE_SQL_QUERY_COMMAND += "`tokens` ON `records`.`operator_id` = `tokens`.`admin_id` LEFT JOIN `jobs` ON `records`.`project_id`"
    ALL_IN_ONE_SQL_QUERY_COMMAND += " = `jobs`.`project_id` AND `records`.`job_id` = `jobs`.`job_id`"

    @staticmethod
    def init_app(app):
        """ensure that restful response should be encode with utf8"""
        app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
