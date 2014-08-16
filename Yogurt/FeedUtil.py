import sys
import json
import functools

from datetime import datetime

from . import AppCache
from . import ServerUtil


class FeedException(Exception):
    def __init__(self, message):
        self.message = message

def restfiyString(string):
    return string.replace(' ', '_')

class Feed(object):
    def __init__(self, **kwargs):
        try:
            self._key = kwargs['key']
        except:
            self._key = None
        try:
            self._base = kwargs['base']
        except:
            self._base = None
        try:
            self._timer = kwargs['timer'] * 60
        except KeyError:
            raise Exception('Feed handler does not provide %s' % sys.exc_info()[1])
        if not hasattr(self, '_key') or not hasattr(self, '_base'):
            raise Exception('Feed handler doesn\'t specify a key or base')

    def __call__(self, func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            ServerUtil.info('>>> Feed Event Calling [%s]' % func.__name__)
            retval = func(*args, **kwargs)
            ServerUtil.info('<<< Feed Event Leaving [%s]' % func.__name__)
            if retval is not None:
                if self._key:
                    AppCache.CacheServer.set(self._key, json.dumps(retval))
                else:
                    if retval is not None:
                        for i in retval.keys():
                            AppCache.CacheServer.set(self._base % restfiyString(i), json.dumps(retval[i]))
        return decorated


class CacheResult:
    def __init__(self, timer=None):
        self._timer = timer
        self._first = True
        self._timestamp = None
        self._retval = None

    def __call__(self, func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            if self._first is True:
                self._retval = func(*args, **kwargs)
                self._first = False
                self._timestamp = datetime.now()
            else:
                if self._timer:
                    now = datetime.now()
                    diff = (now - self._timestamp).seconds * 60
                    if diff >= self._timer:
                        self._retval = func(*args, **kwargs)
                        self._timestamp = ts
            return self._retval
        return decorated
