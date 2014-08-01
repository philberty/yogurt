import sys
import time
import logging
import traceback

from . import YogurtApp
from . import AppCache
from . import ServerUtil

__version__ = '0.1'
__author__ = "Philip Herron"
__email__ = "redbrain@gcc.gnu.org"
__url__ = "https://github.com/redbrain"

def SetupTestEnv (feeds):
    logging.basicConfig (level=logging.INFO)
    AppCache.CacheServer = AppCache.CacheSystem ({'type':'local'}, feeds)
    AppCache.CacheServer.fillup ()

class YogurtServer:
    def __init__ (self, bind, port, cache_config, feeds):
        self.web_bind = bind
        self.web_port = port
        AppCache.CacheServer = AppCache.CacheSystem (cache_config, feeds)
        AppCache.CacheServer.fillup ()

    def listen (self):
        try:
            ServerUtil.info ('[Flask] starting http://%s:%i/' \
                             % (self.web_bind, self.web_port))
            YogurtApp.app.run (host=self.web_bind, port=self.web_port)
        except KeyboardInterrupt:
            ServerUtil.warning ('Caught keyboard interupt stopping')
        except:
            ServerUtil.error ("%s" % traceback.format_exc ())
            ServerUtil.error ("%s" % sys.exc_info () [1])

class YogurtFeeder:
    def __init__ (self, cache_config, feeds):
        AppCache.CacheServer = AppCache.CacheSystem (cache_config, feeds)

    def run (self, timer):
        ServerUtil.info ('Feeding every %s mins' % timer)
        try:
            while True:
                AppCache.CacheServer.fillup ()
                time.sleep (timer * 60)
        except KeyboardInterrupt:
            ServerUtil.info ('Caught Keyboard interupt stopping!')
