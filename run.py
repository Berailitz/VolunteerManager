"""start main app"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
from VolunteerManager import app, mess

application = app.create_app()

def main():
    """main func"""
    mess.set_logger(application, 'log.txt')
    logging.info('start...')
    application.run(port=9020, debug=True)

if __name__ == '__main__':
    main()
