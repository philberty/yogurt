import sys
import json
import time
import asyncio
import functools
import requests

from datetime import datetime

from . import AppCache
from . import ServerUtil

requests.adapters.DEFAULT_RETRIES = 5

class FeedException(Exception):
    def __init__(self, message):
        self.message = message

def restfiyString(string):
    tmp = string
    replaces = [':', '-', ',', ' ']
    for i in replaces:
        tmp = tmp.replace(i, '')
    return str(tmp)

def getTimeStamp():
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

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
   
    def _doFeedCall(self, func, *args, **kwargs):
        ServerUtil.info('>>> Feed Event Calling [%s]' % func.__name__)
        retval = func(*args, **kwargs)
        ServerUtil.info('<<< Feed Event Leaving [%s]' % func.__name__)
        if retval is not None:
            if retval is not None:
                if self._key:
                    retval['__yogurt_timestamp'] = getTimeStamp()
                    AppCache.CacheServer.set(self._key, json.dumps(retval))
                else:
                    for i in retval.keys():
                        retval[i]['__yogurt_timestamp'] = getTimeStamp()
                        AppCache.CacheServer.set(self._base % restfiyString(i),
                                                 json.dumps(retval[i]))

    def __callAsync__(self, func):
        def decorated(*args, **kwargs):
            while True:
                try:
                    self._doFeedCall(func, *args, **kwargs)
                except:
                    ServerUtil.error("Feed [%s] error [%s]" % (func.__name__, sys.exc_info()[1]))
                finally:
                    yield from asyncio.sleep(self._timer)
        return decorated

    def __callSync__(self, func):
        def decorated(*args, **kwargs):
            self._doFeedCall(func, *args, **kwargs)
        return decorated

    __call__ = __callSync__ if AppCache.Testing else __callAsync__

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
                ServerUtil.info ('Setting Cached Result for [%s]' % func.__name__)
                self._first = False
                self._timestamp = datetime.now()
            else:
                if self._timer:
                    now = datetime.now()
                    diff = (now - self._timestamp).seconds * 60
                    if diff >= self._timer:
                        self._retval = func(*args, **kwargs)
                        ServerUtil.info ('Setting new cached result for [%s]' % func.__name__)
                        self._timestamp = ts
            return self._retval
        return decorated
