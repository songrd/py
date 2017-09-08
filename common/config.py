#! /usr/bin/env
# -*- coding:utf-8 -*-

import time 
import os

#数据库错误日志
mysql_log_path = '%s/log/py.%s.log' % (os.getcwd(), time.strftime("%Y%m"))
