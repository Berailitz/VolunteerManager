#!/usr/env/python3
# -*- coding: UTF-8 -*-

from mess import set_logger
<<<<<<< HEAD
from . import create_app
=======
from VolunteerManager import create_app
>>>>>>> 3c302a805d82775cd5978470567076756fa42cfe
# import ptvsd

# ptvsd.enable_attach("passw0", address=('0.0.0.0', 989))
# ptvsd.wait_for_attach()

def main():
    set_logger('log.txt')
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
