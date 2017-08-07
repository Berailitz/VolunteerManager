'''mess like fun_tools, logger'''
import functools
import logging
import random
import string

def fun_logger(text='Fun_logger'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            logging.info('%s:Called %s(%r, %r):', text, func.__name__, args, kw)
            result = func(*args, **kw)
            logging.info('%s:Returned %r:', text, result)
            return result
        return wrapper
    return decorator

generate_random_string = lambda length: ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def set_logger(LogPath):
    logging.basicConfig(level=logging.INFO,
        format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s',
        datefmt='%Y %b %d %H:%M:%S',
        filename=LogPath,
        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("Start ....")
