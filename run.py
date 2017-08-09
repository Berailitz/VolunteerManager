#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
from VolunteerManager import app, mess

def main():
    mess.set_logger('log.txt')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info('start...')
    flask_app = app.create_app()
    flask_app.run(debug=True)

if __name__ == '__main__':
    main()
