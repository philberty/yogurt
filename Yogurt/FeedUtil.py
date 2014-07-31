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
            try:
                ServerUtil.info ('>>> Calling [%s] for key [%s]' % (func.__name__, self.key))
                retval = func (*args, **kwargs)
                ServerUtil.info ('<<< Leaving [%s] for key [%s]' % (func.__name__, self.key))
                if retval is not None:
                    AppCache.CacheServer.set (self.key, json.dumps (retval))
            except:
                ServerUtil.debug ("%s" % traceback.format_exc ())
                ServerUtil.error ("Caught feed process exception [%s:%s]" \
                                  % (sys.exc_info () [0], sys.exc_info () [1]))
        return decorated
