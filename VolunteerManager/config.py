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
    BACKUP_FOLDER = 'backup'
    TOKEN_LENGTH = 32
    MAX_ITEMS_COUNT_PER_PAGE = 200
    ALL_IN_ONE_SQL_QUERY_COMMAND = "SELECT `record_id`, `records`.`user_id`, `project_name`, `job_name`, `working_date`, `working_time`,"
    ALL_IN_ONE_SQL_QUERY_COMMAND += " `record_note`, `operation_time`, `tokens`.`username`, `record_status`, `legal_name`, `student_id`"
    ALL_IN_ONE_SQL_QUERY_COMMAND += " FROM `records` LEFT JOIN `volunteers` ON `records`.`user_id` = `volunteers`.`user_id` LEFT JOIN "
    ALL_IN_ONE_SQL_QUERY_COMMAND += "`tokens` ON `records`.`operator_id` = `tokens`.`admin_id` LEFT JOIN `jobs` ON `records`.`project_id`"
    ALL_IN_ONE_SQL_QUERY_COMMAND += " = `jobs`.`project_id` AND `records`.`job_id` = `jobs`.`job_id`"
    SYNC_UAERNAME = 'scsfire'
    SYNC_ENCRYPTED_PASSWORD = r"VsNl91lWRJpjkVCTVL4j/pa2w1Ij+U0JqNHIoWCYiGZy5+246J+1UDIs+aplYoH4DiHVfk+jkzGDijqc6ZLsb8mhrj"
    SYNC_ENCRYPTED_PASSWORD += r"WOO/CdZ7tD5rn5+Wd6yFgXnRoiaZGAiaAxiPONZuVce11IyOyISchMapiV8b4G8GyREbEg+pcRuhz5Y3Q="
    SYNC_TRUNCATE_TEMP_TABLE_COMMAND = "TRUNCATE `volunteers_temp`"
    SYNC_VOLUNTEER_SQL_COMMAND = "INSERT INTO `volunteers`(`user_id`, `volunteer_id`, `username`, `student_id`, `class_index`, `legal"
    SYNC_VOLUNTEER_SQL_COMMAND += "_name`, `phone`, `email`, `gender`, `age`, `volunteer_time`, `note`) SELECT `volunteers_temp`.`user_"
    SYNC_VOLUNTEER_SQL_COMMAND += "id`, `volunteers_temp`.`volunteer_id`, `volunteers_temp`.`username`, `volunteers_temp`.`student_id`,"
    SYNC_VOLUNTEER_SQL_COMMAND += " `volunteers_temp`.`class_index`, `volunteers_temp`.`legal_name`, `volunteers_temp`.`phone`,`volunte"
    SYNC_VOLUNTEER_SQL_COMMAND += "ers_temp`.`email`, `volunteers_temp`.`gender`, `volunteers_temp`.`age`, `volunteers_temp`.`volunteer"
    SYNC_VOLUNTEER_SQL_COMMAND += "_time`, `volunteers_temp`.`note` FROM `volunteers_temp` ON DUPLICATE KEY UPDATE `volunteer_id` = `vo"
    SYNC_VOLUNTEER_SQL_COMMAND += "lunteers_temp`.`volunteer_id`, `username` = `volunteers_temp`.`username`, `student_id` = `volunteers"
    SYNC_VOLUNTEER_SQL_COMMAND += "_temp`.`student_id`, `class_index` = `volunteers_temp`.`class_index`, `legal_name` = `volunteers_tem"
    SYNC_VOLUNTEER_SQL_COMMAND += "p`.`legal_name`, `phone` = `volunteers_temp`.`phone`, `email` = `volunteers_temp`.`email`, `gender` "
    SYNC_VOLUNTEER_SQL_COMMAND += "= `volunteers_temp`.`gender`, `age` = `volunteers_temp`.`age`, `volunteer_time` = `volunteers_temp`."
    SYNC_VOLUNTEER_SQL_COMMAND += "`volunteer_time`, `note` = `volunteers_temp`.`note`"

    @staticmethod
    def init_app(app):
        """ensure that restful response should be encode with utf8"""
        app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
