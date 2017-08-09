#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
from VolunteerManager import app, mess

application = app.create_app()

def main():
    mess.set_logger('log.txt')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info('start...')
    application.run(debug=True)

if __name__ == '__main__':
    main()
