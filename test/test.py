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

def test():
    """main func"""
    i = 1
    while(True):
        try:
            command = input(f'IN[{i}]: ')
            result = eval(command)
            logging.info(f'OUT[{i}]: {result}')
            i += 1
        except Exception as identifier:
            logging.exception(identifier)

if __name__ == '__main__':
    set_logger('log.txt')
    test()