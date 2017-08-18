"""Manager class for bv2008.cn"""
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import logging
import time
import random
import requests
from bs4 import BeautifulSoup

str_to_int = lambda raw_string: int(raw_string.strip())
strip_raw_data = lambda raw_data: str(raw_data).strip()

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
    logging.info("Start ....")

class Manager(object):
    """Manage volunteers on bv2008, whose `volunteer_list` is a list of objects"""
    def __init__(self):
        self.my_session = requests.Session()
        self.volunteer_list = list()
        # self.login()

    def post(self, url, referer='', **kw):
        """customized post"""
        if not referer:
            referer = 'http://www.bv2008.cn'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': referer,
        }
        post_response = self.my_session.post(url, headers=headers, **kw)
        post_response.encoding = "utf-8-sig"
        return post_response

    def get(self, url, referer='', **kw):
        """customized get"""
        if not referer:
            referer = 'http://www.bv2008.cn'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': referer,
        }
        get_response = self.my_session.get(url, headers=headers, **kw)
        get_response.encoding = "utf-8-sig"
        return get_response

    def login(self, username, encrypted_password):
        """login with encrypted password"""
        if not username or not encrypted_password:
            logging.error('[Failed]No username or password specified.')
            raise KeyError('No username or password specified.')
        login_url = 'http://www.bv2008.cn/app/user/login.php?m=login'
        login_payload = {"uname": username, "upass": encrypted_password}
        login_response = self.post(login_url, data=login_payload)
        login_json = login_response.json()
        if login_json['code'] == 0:
            logging.info("[Succeeded]Login in")
        else:
            logging.info("[Failed]Login in" + login_json['msg'])
        return True

    def scan(self, interval=2, is_random=True):
        """scan for all volunteers"""
        self.volunteer_list = list()
        scanning_url = "http://www.bv2008.cn/app/org/member.mini.php?type=joined&p={0}"
        scanning_homepage = self.get(scanning_url.format(1))
        main_soup = BeautifulSoup(scanning_homepage.text, "lxml")
        max_page = str_to_int(main_soup.select(".pagebar a")[-1].text)
        volunteer_count = str_to_int(main_soup.select(".ptpage")[0].text.split(' ')[4])
        logging.info(f"[Success]Start scanning for {volunteer_count} volunteers @ {max_page} pages.")
        for page_index in range(1, max_page + 1):
            current_page = self.get(scanning_url.format(page_index))
            logging.info(f"[Success]Get page {page_index}.")
            self.volunteer_list += self.prase_list_soap(current_page.text)
            if is_random:
                time.sleep(2 * interval * random.random())
            else:
                time.sleep(interval)
        logging.info("[Success]Scanning completed.")
        return self.volunteer_list

    def save_to_json(self, json_path='volunteer_list.json'):
        """save volunteer_list to json file"""
        with open(json_path, 'w', encoding='utf8') as json_file:
            json.dump(self.volunteer_list, json_file, ensure_ascii=False)

    def save_to_sql(self, sql_url):
        """save records to sql via pandas"""
        pass

    @staticmethod
    def prase_list_soap(raw_text):
        """return volunteers on the page"""
        soup = BeautifulSoup(raw_text, "lxml")
        volunteer_list = list()
        for member_item in [x for x in soup.select("tr") if not x.select("th")]:
            member_info = dict()
            member_info['user_id'] = str_to_int(member_item.select("input")[0]['value'])
            member_info['volunteer_id'] = strip_raw_data(member_item.select("td")[1].text)
            if len(member_item.select("td")[2].contents) == 3:
                member_info['username'] = strip_raw_data(member_item.select("td")[2].contents[0])
                member_info['student_id'] = strip_raw_data(member_item.select("td")[2].contents[-1])
            elif member_item.select("td")[2].contents[0].name == 'br':
                member_info['username'] = ''
                member_info['student_id'] = strip_raw_data(member_item.select("td")[2].contents[-1])
            else:
                member_info['username'] = strip_raw_data(member_item.select("td")[2].contents[0])
                member_info['student_id'] = ''
            member_info['legal_name'] = strip_raw_data(member_item.select("td")[3].text)
            if len(member_item.select("td")[4].contents) == 3:
                member_info['phone'] = strip_raw_data(member_item.select("td")[4].contents[0])
                member_info['email'] = strip_raw_data(member_item.select("td")[4].contents[-1])
            elif member_item.select("td")[4].contents[0].name == 'br':
                member_info['phone'] = ''
                member_info['email'] = strip_raw_data(member_item.select("td")[4].contents[-1])
            else:
                member_info['phone'] = strip_raw_data(member_item.select("td")[4].contents[0])
                member_info['email'] = ''
            if strip_raw_data(member_item.select("td")[5].text)[0] in ['男', '女']:
                member_info['gender'] = strip_raw_data(member_item.select("td")[5].text)[0]
            else:
                member_info['gender'] = ''
            if strip_raw_data(member_item.select("td")[5].text).split('(')[-1].split(')')[0]:
                member_info['age'] = str_to_int(strip_raw_data(member_item.select("td")[5].text).split('(')[1].split(')')[0])
            else:
                member_info['age'] = None
            member_info['volunteer_time'] = float(strip_raw_data(member_item.select("td")[8].text))
            volunteer_list.append(member_info)
            logging.info("[Success]Scanning: %s", member_info)
        return volunteer_list

    def invite(self, project_id, job_id, volunteer_id_list):
        """invite a list of volunteers to a project"""
        invite_url = f'http://www.bv2008.cn/app/opp/opp.my.php?m=invite&item=recruit&opp_id={project_id}&job_id={job_id}'
        invite_payload = {'stype':'local', 'uid[]': volunteer_id_list}
        invite_response = self.post(invite_url, data=invite_payload)
        response_json = invite_response.json()
        logging.info(f"[Unknown]Invite result: {response_json['msg']}")
        return invite_response

    def import_record_text(self, project_id, job_id, id_type, record_text):
        """add records in text, may fail due to frequent imports within 3 hours"""
        # id_type: 1 for user id, 3 for volunteer id, 4 for legal id
        record_url = f'http://www.bv2008.cn/app/opp/opp.my.php?manage_type=0&m=import_hour&item=hour&opp_id={project_id}'
        record_payload = {'content': record_text, 'vol_type': id_type, 'opp_id': project_id, 'job_id': job_id}
        record_response = self.post(record_url, data=record_payload)
        response_json = record_response.json()
        if response_json['code'] == 0:
            logging.info(f"[Succeeded]Record: {response_json['msg']}")
        for recorded_item in response_json['data'][0]:
            success_log = "[Failed]Record: #{vol_id} {hour_num} hour(s) for job #{job_id}, opp #{opp_id}: {msg}".format(**recorded_item)
            logging.info(success_log)
        for failed_item in response_json['failed'][0]:
            error_log = "[Failed]Record: #{vol_id} {hour_num} hour(s) for job #{job_id}, opp #{opp_id}: {msg}".format(**failed_item)
            logging.info(error_log)
        return record_response

    def save_record_item(self, project_id, job_id, user_id, working_time, record_note):
        """save one record"""
        record_url = f'http://www.bv2008.cn/app/opp/opp.my.php?manage_type=0&m=save_hour&item=hour&opp_id={project_id}&job_id={job_id}'
        record_payload = {'hour_num': working_time, 'memo': record_note, 'uid': user_id}
        record_response = self.post(record_url, data=record_payload)
        response_json = record_response.json()
        if response_json['code'] == 0:
            logging.info(f"[Succeeded]Record: #{response_json['id']} {response_json['msg']}")
        else:
            logging.info(f"[Failed]Record: #{response_json['id']} ERROR{response_json['code']} {response_json['msg']}")
        return record_response

def main():
    """main function"""
    set_logger("log.txt")
    encrypted_password = r"VsNl91lWRJpjkVCTVL4j/pa2w1Ij+U0JqNHIoWCYiGZy5+246J+1UDIs+aplYoH4DiHVfk+jkzGDijqc6ZLsb8mhrj"
    encrypted_password += r"WOO/CdZ7tD5rn5+Wd6yFgXnRoiaZGAiaAxiPONZuVce11IyOyISchMapiV8b4G8GyREbEg+pcRuhz5Y3Q="
    my_manager = Manager()
    my_manager.login("scsfire", encrypted_password)
    # hours = my_manager.get(r"http://www.bv2008.cn/app/opp/opp.my.php?item=hour&job_id=1112895&opp_id=844088&type=hlist&manage_type=0")
    # hour_soup = BeautifulSoup(hours, "lxml")
    # hour_soup.find("a")
    # my_manager.scan()

if __name__ == '__main__':
    main()
