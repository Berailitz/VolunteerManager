"""mess like fun_tools, logger"""
import functools
import logging
import os
import os.path as path
import random
import string
import zipfile
from logging.handlers import RotatingFileHandler

def fun_logger(text='Fun_logger'):
    """log function call and result with custom text head"""
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
str_to_int = lambda raw_string: int(raw_string.strip())
strip_raw_data = lambda raw_data: str(raw_data).strip()

def set_logger(log_path):
    """Adapt to Flask, log into log file at `log_path`, at level `INFO`"""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s',
        datefmt='%Y %b %d %H:%M:%S',
        filename=log_path,
        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=5, encoding='utf8')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    logging.getLogger(None).addHandler(console)
    logging.getLogger(None).addHandler(file_handler)
    logging.info("Start ....")

def zip_a_file(raw_file_path, zip_file_path=None, open_mode='w', delete_after_zip=False):
    """ NOTE: All path must be absolute path. and Add `raw_file` into `zip_file`. `raw_file` must be readable and
    folder of `zip_file` will be created if not exist. File `zip_file_path` will be truncated if both it exists and
    `open_mode` is `w` (default), or appended if `open_mode` is `a`. Raw file will be deleted if `delete_after_zip`."""
    if not zip_file_path:
        zip_file_path = path.join(path.dirname(raw_file_path), path.basename(raw_file_path).split('.')[0] + '.zip')
    os.makedirs(path.dirname(zip_file_path), exist_ok=True)
    with zipfile.ZipFile(zip_file_path, mode=open_mode, compression=zipfile.ZIP_DEFLATED) as zip_file_object:
        zip_file_object.write(raw_file_path)
    if delete_after_zip:
        os.remove(raw_file_path)
    return zip_file_path
