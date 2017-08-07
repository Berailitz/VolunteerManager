#!/usr/env/python3
# -*- coding: UTF-8 -*-

import ptvsd

ptvsd.enable_attach("passw0", address=('0.0.0.0', 989))
ptvsd.wait_for_attach()

print('ok')
