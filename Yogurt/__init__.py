import sys
import time
import logging
import traceback
import threading

from . import AppCache
from . import YogurtApp
from . import ServerUtil

__version__ = '0.1'
__author__ = "Philip Herron"
__email__ = "redbrain@gcc.gnu.org"
__url__ = "https://github.com/redbrain"


def setupTestEnviroment():
    AppCache.CacheServer = AppCache.CacheSystem({'type': 'local'})
    return AppCache.CacheServer

class YogurtServer:
    def __init__(self, bind, port, cache_config):
        self.web_bind = bind
        self.web_port = port
        AppCache.CacheServer = AppCache.CacheSystem(cache_config)

    def listen(self):
        try:
            ServerUtil.info('[Flask] starting http://%s:%i/' % (self.web_bind, self.web_port))
            YogurtApp.app.run(host=self.web_bind, port=self.web_port)
        except KeyboardInterrupt:
            ServerUtil.warning('Caught keyboard interrupt stopping')
        except:
            ServerUtil.error("%s" % traceback.format_exc())
            ServerUtil.error("%s" % sys.exc_info()[1])


class YogurtFeeder:
    def __init__(self, cache_config, feeds):
        AppCache.CacheServer = AppCache.CacheSystem(cache_config, feeds=feeds)

    def run(self):
        ServerUtil.info('Feeding...')
        try:
            AppCache.CacheServer.incubate()
        except KeyboardInterrupt:
            ServerUtil.info('Caught Keyboard interrupt stopping!')
