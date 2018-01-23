#!/usr/bin/env python3
# dependencies
import sys
from datetime import datetime
from weibo import Weibo

# configuration parameters
from config import cookie
from config import filter
from config import user_id
from config import connection_timeout
from config import pause_interval
from config import pause_time

# 更新微博
w = Weibo(user_id,filter=0)
w.set_cookie(cookie)
w.connection_timeout = connection_timeout
w.pause_interval = pause_interval
w.pause_time = pause_time
w.update()

# 创建新的timeline
from timeline import build_timeline
build_timeline(user_id, template_name="PinkStar")