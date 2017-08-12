"""Manager class for bv2008.cn"""
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import logging
import time
import random
import requests
from bs4 import BeautifulSoup
from .config import AppConfig, app_status_dict
from .mess import str_to_int, strip_raw_data
from .sql_handle import export_to_json, import_volunteers

class SyncManager(object):
    """Manage volunteers on bv2008, whose `volunteer_list` is a list of objects. Call `login` before doing anything else."""
    def __init__(self):
        self.my_session = requests.Session()
        self.volunteer_list = list()

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

    def post(self, url, referer='http://www.bv2008.cn', **kw):
        """customized post"""
        post_response = self.my_session.post(url, headers=self.create_headers(referer), **kw)
        post_response.encoding = "utf-8-sig"
        return post_response

    def get(self, url, referer='http://www.bv2008.cn', **kw):
        """customized get"""
        get_response = self.my_session.get(url, headers=self.create_headers(referer), **kw)
        get_response.encoding = "utf-8-sig"
        return get_response

    def login(self, username, encrypted_password):
        """login with encrypted password"""
        if not username or not encrypted_password:
            logging.error('No username or password specified.')
            raise KeyError('No username or password specified.')
        login_url = 'http://www.bv2008.cn/app/user/login.php?m=login'
        login_payload = {"uname": username, "upass": encrypted_password}
        login_response = self.post(login_url, data=login_payload)
        login_json = login_response.json()
        if login_json['code'] == 0:
            logging.info(f"Login as {username}")
            return True
        else:
            logging.error(f"Faied to login: {login_json['msg']}")
            return False

    def scan(self, interval=2, max_volunteers_count=None, save_on_the_fly=False):
        """NOTE: DEBUG: scan for all volunteers"""
        self.volunteer_list = list()
        scanning_url = "http://www.bv2008.cn/app/org/member.mini.php?type=joined&p={0}"
        scanning_homepage = self.get(scanning_url.format(1))
        main_soup = BeautifulSoup(scanning_homepage.text, "lxml")
        max_page = str_to_int(main_soup.select(".pagebar a")[-1].text)
        expected_volunteer_count = str_to_int(main_soup.select(".ptpage")[0].text.split(' ')[4])
        accumulated_volunteer_count = 0
        logging.info(f"Start scanning for {expected_volunteer_count} volunteers @ {max_page} pages.")
        for page_index in range(1, max_page + 1):
            logging.info(f"Getting page {page_index}.")
            current_page = self.get(scanning_url.format(page_index))
            if save_on_the_fly:
                self.volunteer_list = self.prase_list_soap(current_page.text)
                accumulated_volunteer_count += len(self.volunteer_list)
                self.save_to_sql()
                app_status_dict['syncing_process_volunteers'] = f'{accumulated_volunteer_count}/{expected_volunteer_count}'
            else:
                self.volunteer_list += self.prase_list_soap(current_page.text)
                accumulated_volunteer_count = len(self.volunteer_list)
            if max_volunteers_count and accumulated_volunteer_count >= max_volunteers_count: # NOTE: for DEBUG
                break
            time.sleep(2 * interval * random.random())
        logging.info(f"Scanned {accumulated_volunteer_count}/{expected_volunteer_count} volunteer(s).")

    @staticmethod
    def prase_list_soap(raw_text):
        """receive text, return volunteers on the page, by `list` of `dict`s"""
        soup = BeautifulSoup(raw_text, "lxml")
        volunteer_list = list()
        for member_item in [x for x in soup.select("tr") if not x.select("th")]:
            member_info = dict()
            member_info['user_id'] = member_item.select("input")[0]['value']
            td_list = member_item.select("td")
            member_info['volunteer_id'] = td_list[1].text
            if len(td_list[2].contents) == 3:
                member_info['username'] = td_list[2].contents[0]
                member_info['student_id'] = td_list[2].contents[-1]
            elif td_list[2].contents[0].name == 'br':
                member_info['username'] = ''
                member_info['student_id'] = td_list[2].contents[-1]
            else:
                member_info['username'] = td_list[2].contents[0]
                member_info['student_id'] = ''
            member_info['legal_name'] = td_list[3].text
            if len(td_list[4].contents) == 3:
                member_info['phone'] = td_list[4].contents[0]
                member_info['email'] = td_list[4].contents[-1]
            elif td_list[4].contents[0].name == 'br':
                member_info['phone'] = ''
                member_info['email'] = td_list[4].contents[-1]
            else:
                member_info['phone'] = td_list[4].contents[0]
                member_info['email'] = ''
            gender_and_age = strip_raw_data(td_list[5].text)
            if gender_and_age[0] in ['男', '女']:
                member_info['gender'] = gender_and_age[0]
            else:
                member_info['gender'] = ''
            if gender_and_age.split('(')[-1].split(')')[0]:
                member_info['age'] = gender_and_age.split('(')[1].split(')')[0]
            else:
                member_info['age'] = None
            member_info['volunteer_time'] = float(strip_raw_data(td_list[8].text))
            for key_of_text in ['volunteer_id', 'username', 'student_id', 'legal_name', 'phone', 'email', 'gender']:
                member_info[key_of_text] = strip_raw_data(member_info[key_of_text])
            for key_of_int in ['user_id', 'age']:
                member_info[key_of_int] = str_to_int(member_info[key_of_int])
            volunteer_list.append(member_info)
            logging.info("Scanning: %s", member_info)
        if volunteer_list:
            logging.info(f'Prased {len(volunteer_list)} volunteer(s).')
        else:
            logging.error('No volunteer prased.')
        return volunteer_list

    def save_to_json(self, json_path='volunteer_list.json', custom_volunteer_list=None):
        """save volunteer_list to json file, which will be truncating if it exists, or created otherwise."""
        with open(json_path, 'w', encoding='utf8') as json_file:
            if custom_volunteer_list:
                json.dump(custom_volunteer_list, json_file, ensure_ascii=False)
            else:
                json.dump(self.volunteer_list, json_file, ensure_ascii=False)

    def save_to_sql(self, custom_volunteer_list=None):
        """save records to sql invoking `import_to_sql` via `pandas`"""
        if custom_volunteer_list:
            import_volunteers(custom_volunteer_list)
        else:
            import_volunteers(self.volunteer_list)

    def invite(self, project_id, job_id, volunteer_id_list):
        """invite a list of volunteers to a project"""
        invite_url = f'http://www.bv2008.cn/app/opp/opp.my.php?m=invite&item=recruit&opp_id{project_id}&job_id={job_id}'
        invite_payload = {'stype':'local', 'uid[]': volunteer_id_list}
        invite_response = self.post(invite_url, data=invite_payload)
        response_json = invite_response.json()
        logging.info(f"Invite info: {response_json['msg']}")
        return invite_response

    def import_record_text(self, project_id, job_id, id_type, record_text):
        """add records in text, may fail due to frequent imports within 3 hours"""
        # id_type: 1 for user id, 3 for volunteer id, 4 for legal id
        record_url = f'http://www.bv2008.cn/app/opp/opp.my.php?manage_type=0&m=import_hour&item=hour&opp_id={project_id}'
        record_payload = {'content': record_text, 'vol_type': id_type, 'opp_id': project_id, 'job_id': job_id}
        record_response = self.post(record_url, data=record_payload)
        response_json = record_response.json()
        if response_json['code'] == 0:
            logging.info(f"Record: {response_json['msg']}")
        for recorded_item in response_json['data'][0]:
            logging.info("Record: #%(vol_id)s %(hour_num)s hour(s) for job #%(job_id)s, opp #%(opp_id)s: %(msg)s", **recorded_item)
        for error_item in response_json['ERROR'][0]:
            logging.error("Record: #%(vol_id)s %(hour_num)s hour(s) for job #%(job_id)s, opp #%(opp_id)s: %(msg)s", **error_item)
        return response_json

    def save_record_item(self, project_id, job_id, user_id, working_time, record_note):
        """save one record"""
        record_url = f'http://www.bv2008.cn/app/opp/opp.my.php?manage_type=0&m=save_hour&item=hour&opp_id={project_id}&job_id={job_id}'
        record_payload = {'hour_num': working_time, 'memo': record_note, 'uid': user_id}
        record_response = self.post(record_url, data=record_payload)
        response_json = record_response.json()
        if response_json['code'] == 0:
            logging.info(f"Record: #{response_json['id']} {response_json['msg']}")
        else:
            logging.error(f"Record: #{response_json['id']} ERROR{response_json['code']} {response_json['msg']}")
        return response_json

sync_helper = SyncManager()

def sync_volunteer_info():
    """DEBUG: limitation of 20 volunteers. Backup sql to zipped json, scan volunteers and save to `volunteers`"""
    syncing_status = app_status_dict['is_syncing_volunteers']
    operation_dict = {
        'finished': sync_volunteer_execute,
        'underway': lambda: '同步未结束',
        'error': lambda: '同步出错',
    }
    return operation_dict[syncing_status]()

def sync_volunteer_execute():
    """PRIVATE: sync volunteers"""
    app_status_dict['is_syncing_volunteers'] = 'underway'
    export_to_json('volunteers')
    sync_helper.login(AppConfig.SYNC_UAERNAME, AppConfig.SYNC_ENCRYPTED_PASSWORD)
    sync_helper.scan(2, max_volunteers_count=20, save_on_the_fly=True)
    app_status_dict['is_syncing_volunteers'] = 'finished'
    return None
