#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:   fanzeyi
# CREATED:  17:16:23 14/07/2013
# MODIFIED: 17:48:29 14/07/2013

PASSWD = ""
URL_LENGTH = 4
MAX_RETRY_TIME = 5
SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/zris.db"

try:
    from local_config import *
except Exception:
    pass
