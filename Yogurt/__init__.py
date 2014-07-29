import sys
import time
import traceback
import ServerUtil

import AppCache
import YogurtApp

from gevent.pywsgi import WSGIServer

version = '0.1'

class YogurtServer:
    def __init__ (self, bind, port, cache_config, feeds):
        self.web_bind = bind
        self.web_port = port
        AppCache.CacheServer = AppCache.CacheSystem (cache_config, feeds)
        AppCache.CacheServer.fillup ()

    def listen (self):
        try:
            ServerUtil.info ('WSGIServer:[gevent] starting http://%s:%i/' \
                             % (self.web_bind, self.web_port))
            http_server = WSGIServer ((self.web_bind, self.web_port), YogurtApp.app)
            http_server.serve_forever ()
        except KeyboardInterrupt:
            ServerUtil.warning ('Caught keyboard interupt stopping')
        except:
            ServerUtil.error ("%s" % traceback.format_exc ())
            ServerUtil.error ("%s" % sys.exc_info () [1])

class YogurtFeeder:
    def __init__ (self, feeds, cache_config):
        AppCache.CacheServer = AppCache.CacheSystem (cache_config, feeds)

    def run (self, timer):
        if timer is None:
            AppCache.CacheServer.fillup ()
        else:
            ServerUtil.info ('Feeding every %s mins' % timer)
            try:
                while True:
                    AppCache.CacheServer.fillup ()
                    time.sleep (timer * 60)
            except KeyboardInterrupt:
                ServerUtil.info ('Caught Keyboard interupt stopping!')
