import json
import time

from . import ServerUtil
from . import RedisCache
from . import LocalCache

CacheServer = None
class CacheSystem:
    def __init__ (self, config, feeds):
        self.feeds = feeds
        self.type = config ['type'].lower ()
        if self.type == 'redis':
            self.__cache = RedisCache.Cache (config)
        elif self.type == 'local':
            self.__cache = LocalCache.Cache (config)
        else:
            raise Exception ('Uknown cache type [%s]' % self.type)
        self.__cache.set ("__yogurt_test","ping")

    def fillup (self, ignore=True):
        ServerUtil.info ('Initilizing app cache')
        try:
            for i in self.feeds:
                feeds = filter (lambda x: x.startswith ('Feed_'), dir (i))
                for y in feeds:
                    getattr (i, y) ()
        except:
            if not ignore:
                raise
        ServerUtil.info ('Cache initilization done!')

    def get (self, key):
        return self.__cache.get (key)

    def set (self, key, value):
        return self.__cache.set (key, value)

