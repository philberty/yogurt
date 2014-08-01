import sys
import json
import functools
import traceback

from . import AppCache
from . import ServerUtil

class Feed (object):
    def __init__ (self, **kwargs):
        try:
            self.key = kwargs ['key']
        except KeyError:
            raise FeedException ('Feed handler %s does not provide a key' % func)

    def __call__ (self, func):
        @functools.wraps (func)
        def decorated (*args, **kwargs):
            ServerUtil.info ('>>> Calling [%s] for key [%s]' % (func.__name__, self.key))
            retval = func (*args, **kwargs)
            ServerUtil.info ('<<< Leaving [%s] for key [%s]' % (func.__name__, self.key))
            if retval is not None:
                AppCache.CacheServer.set (self.key, json.dumps (retval))
        return decorated
