'''mess like fun_tools, logger'''
import functools
import logging
import random
import string

def fun_logger(text='Fun_logger'):
    '''log function call and result with custom text head'''
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

def set_logger(log_path):
    '''log into log file at `log_path`, at level `INFO`'''
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s',
        datefmt='%Y %b %d %H:%M:%S',
        filename=log_path,
        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info("Start ....")
