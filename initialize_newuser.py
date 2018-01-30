#!/usr/bin/env python3
# dependencies
import sys
from datetime import datetime
from weibo import Weibo

# configuration parameters
from config import cookie
from config import filter
from config import connection_timeout
from config import pause_interval
from config import pause_time

# 更新微博
w = Weibo(5461287018,filter=0)
w.set_cookie(cookie)
w.connection_timeout = connection_timeout
w.pause_interval = pause_interval
w.pause_time = pause_time
w.start()
