"""test `scan` in `sync_helper`, to be run at `/` """
#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from test_mess import test_mess
from VolunteerManager import config, mess, sync_helper

def main():
    """main test"""
    mess.set_logger('log.txt')
    Ma = sync_helper.SyncManager()
    Ma.login(config.AppConfig.SYNC_UAERNAME, config.AppConfig.SYNC_ENCRYPTED_PASSWORD)
    test_mess.exec_test([Ma])

if __name__ == '__main__':
    main()
