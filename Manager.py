'''Manager class for bv2008.cn'''
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import logging
import time
import random
import requests
from bs4 import BeautifulSoup

def set_logger(log_file_path):
    '''set logger'''
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
    """Manage volunteers on bv2008"""
    def __init__(self):
        self.my_session = requests.Session()
        self.login()

    def post(self, url, referer='', **kw):
        '''customized post'''
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
        '''customized get'''
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

    def login(self, username="scsfire", encrypted_password=""):
        '''login with default password'''
        if not encrypted_password:
            encrypted_password = r"VsNl91lWRJpjkVCTVL4j/pa2w1Ij+U0JqNHIoWCYiGZy5+246J+1UDIs+aplYoH4DiHVfk+jkzGDijqc6ZLsb8mhrj"
            encrypted_password = encrypted_password + r"WOO/CdZ7tD5rn5+Wd6yFgXnRoiaZGAiaAxiPONZuVce11IyOyISchMapiV8b4G8GyREbEg+pcRuhz5Y3Q="
        url = r'http://www.bv2008.cn/app/user/login.php?m=login'
        payload = {"uname": username, "upass": encrypted_password,}
        response = self.post(url, data=payload)
        if response.json()['code'] == 0:
            logging.info("[Succeed]Login in")
        else:
            logging.info("[Failed]Login in" + response.json()['msg'])

    def scan(self, interval=0.5, is_random=1):
        '''scan for all volunteers'''
        volunteer_list = list()
        url = r"http://www.bv2008.cn/app/org/member.mini.php?type=joined&p="
        homepage = self.get(url + '1')
        main_soup = BeautifulSoup(homepage.text, "lxml")
        max_page = int(main_soup.select(".pagebar a")[-1].text)
        volunteer_count = int(main_soup.select(".ptpage")[0].text.split(' ')[4])
        logging.info("[Success]Scanning " + str(volunteer_count) + " volunteers @ " + str(max_page) + " pages.")
        for page_index in range(1, max_page + 1):
            current_page = self.get(url + str(page_index))
            logging.info("[Success]Get page " + str(page_index) + ".")
            volunteer_list = volunteer_list + self.prase_list_soap(BeautifulSoup(current_page.text, "lxml"))
            if is_random:
                time.sleep(interval * random.random())
            else:
                time.sleep(interval)
        with open("volunteer_list.json", 'w', encoding='utf8') as json_file:
            json.dump(volunteer_list, json_file, ensure_ascii=False)
        logging.info("[Success]Scanning completed.")
        return volunteer_list

    @staticmethod
    def prase_list_soap(soup):
        '''return volunteers on the page'''
        volunteer_list = list()
        for member_item in [x for x in soup.select("tr") if not x.select("th")]:
            member_info = list()
            member_info.append(member_item.select("input")[0]['value'])
            member_info.append(member_item.select("td")[1].text)
            # print(len(member_item.select("td")[2].contents))
            # print(member_item.select("td")[2].contents)
            if len(member_item.select("td")[2].contents) == 3:
                member_info.append(str(member_item.select("td")[2].contents[0]))
                member_info.append(str(member_item.select("td")[2].contents[-1]))
            elif member_item.select("td")[2].contents[0].name == 'br':
                member_info.append('')
                member_info.append(str(member_item.select("td")[2].contents[-1]))
            else:
                member_info.append(str(member_item.select("td")[-1].contents[0]))
                member_info.append('')
            member_info.append(member_item.select("td")[3].text)
            # print(len(member_item.select("td")[4].contents))
            # print(member_item.select("td")[4].contents)
            if len(member_item.select("td")[4].contents) == 3:
                member_info.append(str(member_item.select("td")[4].contents[0]))
                member_info.append(str(member_item.select("td")[4].contents[-1]))
            elif member_item.select("td")[4].contents[0].name == 'br':
                member_info.append('')
                member_info.append(str(member_item.select("td")[4].contents[-1]))
            else:
                member_info.append(str(member_item.select("td")[4].contents[0]))
                member_info.append('')
            if member_item.select("td")[5].text[0] == '男' or member_item.select("td")[5].text[0] == '女':
                member_info.append(member_item.select("td")[5].text[0])
            else:
                member_info.append('')
            if member_item.select("td")[5].text.split('(')[1].split(')')[0]:
                member_info.append(member_item.select("td")[5].text.split('(')[1].split(')')[0])
            else:
                member_info.append('')
            member_info.append(member_item.select("td")[8].text)
            member_info = list(map(lambda text: text.strip(), member_info))
            volunteer_list.append(member_info)
            logging.info("[Success]Scanning: " + '|'.join(map(str, member_info)))
        return volunteer_list

    def invite(self, project_id, job_id, volunteer_id_list):
        '''invite volunteers to a project'''
        invite_url = r'http://www.bv2008.cn/app/opp/opp.my.php?m=invite&item=recruit&opp_id=' + str(project_id) + '&job_id=' + str(job_id)
        invite_payload = {'stype':'local', 'uid[]': volunteer_id_list}
        invite_response = self.post(invite_url, data=invite_payload)
        logging.info("[Succeed]Invite info: " + invite_response.json()['msg'])
        return invite_response

    def record(self, project_id, job_id, id_type, record_text):
        '''add records in text'''
        # id_type: 1 for user id, 3 for volunteer id, 4 for legal id
        record_url = r'http://www.bv2008.cn/app/opp/opp.my.php?manage_type=0&m=import_hour&item=hour&opp_id=' + str(project_id)
        record_payload = {'content': record_text, 'vol_type': id_type, 'opp_id': project_id, 'job_id': job_id}
        record_response = self.post(record_url, data=record_payload)
        if record_response.json()['code'] == 0:
            logging.info("[Succeed]Record: " + record_response.json()['msg'])
        for recorded_item in record_response.json()['data'][0]:
            success_log = "[Succeed]Record: " + recorded_item['vol_id'] + "@" + recorded_item['hour_num']
            success_log = success_log + " " + recorded_item['job_id'] + "@" + recorded_item['opp_id']
            success_log = success_log + ": " +recorded_item['msg']
            logging.info(success_log)
        for failed_item in record_response.json()['failed'][0]:
            error_log = "[Failed]Record: " + failed_item['vol_id'] + "@" + failed_item['hour_num']
            error_log = error_log + " " + failed_item['job_id'] + "@" + failed_item['opp_id']
            error_log = error_log + ": " +failed_item['msg']
            logging.info(error_log)
        return record_response

def main():
    '''main function'''
    set_logger("log.txt")
    my_manager = Manager()
    my_manager.scan()

main()
