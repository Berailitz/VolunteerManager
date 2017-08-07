#!/usr/env/python3
# -*- coding: UTF-8 -*-

from app import createApp
from mess import set_logger
import ptvsd

ptvsd.enable_attach("passw0", address=('0.0.0.0', 989))
#ptvsd.wait_for_attach()

def main():
    set_logger('log.txt')
    app = createApp()
    app.run(debug=True)

if __name__ == '__main__':
    main()
