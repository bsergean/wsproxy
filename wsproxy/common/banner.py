'''Print a banner
'''

import psutil
import os
import time
import platform
from wsproxy.common.version import getVersion


def getBanner():
    p = psutil.Process(os.getpid())
    createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time()))

    banner = r'''
WS_PROXY

WebSocket proxy written in Python3

Version {}
Running on {}
Start time {}
    '''.format(
        getVersion(), platform.uname().node, createTime
    )
    return banner
