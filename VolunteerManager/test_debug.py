#!/usr/env/python3
# -*- coding: UTF-8 -*-

import time
import ptvsd

# ptvsd.settrace("passw0", address=('0.0.0.0', 989), certfile='/etc/letsencrypt/live/ohhere.xyz/fullchain.pem', keyfile='/etc/letsencrypt/live/ohhere.xyz/key.pem')
ptvsd.enable_attach("passw0", address=('0.0.0.0', 989), certfile='/etc/letsencrypt/live/ohhere.xyz/fullchain.pem', keyfile='/etc/letsencrypt/live/ohhere.xyz/key.pem')
print('start')
ptvsd.wait_for_attach() 
time.sleep(1)

print('ok')
