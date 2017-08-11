#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging

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
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Start ....")

def exec_test(env_list=None):
    """test with eval"""
    logging.info('env_list: %r', env_list)
    i = 1
    while True:
        try:
            command = input(f'IN[{i}]: ')
            exec(command)
            i += 1
        except Exception as identifier:
            logging.exception(identifier)
