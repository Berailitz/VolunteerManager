"""Portable manager class for `bv2008.cn`"""
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import functools
import logging
import os
import random
import sys
import time
try:
    import requests
except ImportError as requests_import_error:
    print(requests_import_error.msg)
    requests_import_error.msg = "Please make sure to install package `requests` first."
    requests_import_error.msg += " Run `pip install requests` or"
    requests_import_error.msg += " refer to `http://docs.python-requests.org/zh_CN/latest/user/install.html#install`."
    raise requests_import_error

SYNC_UAERNAME = 'scsfire'
SYNC_ENCRYPTED_PASSWORD = r"VsNl91lWRJpjkVCTVL4j/pa2w1Ij+U0JqNHIoWCYiGZy5+246J+1UDIs+aplYoH4DiHVfk+jkzGDijqc6ZLsb8mhrj"
SYNC_ENCRYPTED_PASSWORD += r"WOO/CdZ7tD5rn5+Wd6yFgXnRoiaZGAiaAxiPONZuVce11IyOyISchMapiV8b4G8GyREbEg+pcRuhz5Y3Q="

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
    logging.info("Start ...")

def auto_login(func):
    """#DEBUG Login before call real method."""
    @functools.wraps(func)
    def wrapper(instance, *args, **kw):
        """update token or set invalid token to ``"""
        if instance.login(SYNC_UAERNAME, SYNC_ENCRYPTED_PASSWORD):
            logging.info('Login to `bv2008.cn`.')
            response = func(instance, *args, **kw)
        else:
            logging.error('Cannot login to `bv2008.cn`.')
            response = None
        return response
    return wrapper

class Manager(object):
    """Manage volunteers on bv2008, whose `volunteer_list` is a list of objects"""
    def __init__(self):
        self.my_session = requests.Session()
        self.volunteer_list = list()
        self.json_path = 'volunteer_list.json'

    @staticmethod
    def create_headers(referer):
        """create http headers with custom `referer`"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': referer,
        }
        return headers

    def post(self, url, data, timeout=10, max_retries=10, referer='http://www.bv2008.cn', **kw):
        """customized post"""
        for attempt_times in range(max_retries):
            try:
                post_response = self.my_session.post(url, headers=self.create_headers(referer), data=data, timeout=timeout, **kw)
                break
            except requests.Timeout as identifier:
                attempt_times += 1
                logging.warning(f'Syncer failed to POST `{str(data)}` to `{url}`: {str(identifier)}')
        post_response.encoding = "utf-8-sig"
        return post_response

    def get(self, url, timeout=10, max_retries=10, referer='http://www.bv2008.cn', **kw):
        """customized get"""
        for attempt_times in range(max_retries):
            try:
                get_response = self.my_session.get(url, headers=self.create_headers(referer), timeout=timeout, **kw)
                break
            except requests.Timeout as identifier:
                attempt_times += 1
                logging.warning(f'Syncer failed to GET `{url}`: {str(identifier)}')
        get_response.encoding = "utf-8-sig"
        return get_response

    def login(self, username, encrypted_password):
        """login with encrypted password"""
        if not username or not encrypted_password:
            logging.error('[Failed]No username or password specified.')
            raise KeyError('No username or password specified.')
        login_url = 'http://www.bv2008.cn/app/user/login.php?m=login'
        login_payload = {"uname": username, "upass": encrypted_password}
        login_response = self.post(login_url, login_payload)
        login_json = login_response.json()
        if login_json['code'] == 0:
            logging.info(f"[Succeeded]Login as {username}")
            return True
        else:
            logging.error(f"[Failed]Faied to login: {login_json['msg']}")
            return False

    def invite(self, project_id, job_id, volunteer_id_list):
        """invite a list of volunteers to a project"""
        invite_url = f'http://www.bv2008.cn/app/opp/opp.my.php?m=invite&item=recruit&opp_id={project_id}&job_id={job_id}'
        invite_payload = {'stype':'local', 'uid[]': volunteer_id_list}
        invite_response = self.post(invite_url, invite_payload)
        response_json = invite_response.json()
        logging.info(f"[Unknown]Invite info: {response_json['msg']}")
        return invite_response.json()

    def import_record_text(self, project_id, job_id, id_type, record_text):
        """#DEBUG#: add records in text, may fail due to frequency limits"""
        # id_type: 1 for user id, 3 for volunteer id, 4 for legal id
        record_url = f'http://www.bv2008.cn/app/opp/opp.my.php?manage_type=0&m=import_hour&item=hour&opp_id={project_id}'
        record_payload = {'content': record_text, 'vol_type': id_type, 'opp_id': project_id, 'job_id': job_id}
        record_response = self.post(record_url, record_payload)
        response_json = record_response.json()
        logging.info("import_record_text -> response_json: " + str(response_json)) # for debug
        if response_json['code'] == 0:
            logging.info(f"[Unknown]Record: {response_json['msg']}")
        if 'data' in response_json.keys():
            for recorded_item in response_json['data']:
                success_log = "[Successful]: #{vol_id} -> {hour_num} hours @ job #{job_id}, opp #{opp_id}: {msg}".format(**recorded_item)
                logging.info(success_log)
        if 'failed' in response_json.keys():
            for failed_item in response_json['failed']:
                error_log = "[Failed]: #{vol_id} -> {hour_num} hours @ job #{job_id}, opp #{opp_id}: {msg}".format(**failed_item)
                logging.error(error_log)
        return response_json

    def save_record_item(self, project_id, job_id, user_id, working_time, record_note):
        """save one record"""
        record_url = f'http://www.bv2008.cn/app/opp/opp.my.php?manage_type=0&m=save_hour&item=hour&opp_id={project_id}&job_id={job_id}'
        record_payload = {'hour_num': str(working_time), 'memo': str(record_note), 'uid[]': str(user_id)}
        record_response = self.post(record_url, record_payload)
        response_json = record_response.json()
        logging.info("save_record_item -> response_json: " + str(response_json)) # for debug
        if response_json['code'] == 0:
            logging.info(f"[Successful]Record: {response_json['msg']}")
        else:
            logging.info(f"[Failed]Record: #{response_json['id']} ERROR{response_json['code']} {response_json['msg']}")
        return response_json

    @auto_login
    def generate_hour_code(self, project_id, job_id, code_amount, code_hour, code_note='', code_uid=[]):
        """#DEBUG `uid` or `uid[]` or None. #TODO: check response. `code_uid` is reserved (useless)."""
        save_code_url = f'http://www.bv2008.cn/app/opp/opp.my.php'
        save_code_params = {'manage_type': '0', 'm': 'save_hour_code', 'item': 'hour', 'opp_id': project_id, 'job_id': job_id}
        save_code_payload = {'job_id': job_id, 'hc_total': code_amount, 'hc_hour': code_hour, 'memo': code_note, 'uid[]': code_uid}
        save_code_response = self.post(save_code_url, data=save_code_payload, params=save_code_params)
        response_json = save_code_response.json()
        logging.debug(f'generate_hour_code->response_json: {response_json}')
        if response_json['code'] == 0:
            logging.info(f"[Successful]Record: {response_json['msg']}")
        else:
            logging.error(f"[Failed]Record: #{response_json['id']} ERROR{response_json['code']}: {response_json['msg']}")
        return response_json

    @auto_login
    def get_hour_code(self, project_id, job_id, folder_path=''):
        """#DEBUG #TODO: Download code file to temp folder."""
        module_dir = os.path.split(os.path.realpath(__file__))[0]
        current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        filename = f'hour_code_{project_id}_{job_id}_{current_time}_LOCAL.xls'
        real_path = os.path.join(module_dir, folder_path, filename)
        download_url = f'http://www.bv2008.cn/app/opp/opp.my.php'
        download_params = {'item': 'hour', 'opp_id': project_id, 'job_id': job_id, 'm': 'export_excel_hcode', 'manage_type': '0'}
        excel_response = self.get(download_url, params=download_params)
        with open(real_path, 'wb') as temp_file:
            temp_file.write(excel_response.content)
        return filename

def main():
    """main function"""
    ###################################################################
    ########################只需修改下面几行############################
    my_volunteer_uid_list = [27140874, 27264014, 27299558] #志愿者的UID
    my_project_id = 1164518 #项目ID
    my_job_id = 1495453 # 岗位ID
    my_hour = 6 # 时长
    my_note = "这里写备注" # 备注
    ########################只需修改上面几行############################
    ###################################################################
    set_logger("volunteer_log.txt")
    if sys.version_info < (3, 6):
        raise RuntimeError('Please install Python 3.6.2 or above. See `https://www.python.org/getit/`')
    time_to_sleep = 3
    my_manager = Manager()
    login_status = my_manager.login(SYNC_UAERNAME, SYNC_ENCRYPTED_PASSWORD)
    if not login_status:
        exit()
    my_manager.invite(my_project_id, my_job_id, my_volunteer_uid_list)
    for single_volunteer_uid in my_volunteer_uid_list:
        my_manager.save_record_item(my_project_id, my_job_id, single_volunteer_uid, my_hour, my_note)
        time.sleep(2 * time_to_sleep * random.random())
    logging.info("Done.")
    logging.info("Please check if there is any error in `volunteer_log.txt`.")
    input("Press `Enter` to exit.")

if __name__ == '__main__':
    main()
