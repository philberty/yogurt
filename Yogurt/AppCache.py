import json

from . import RedisCache
from . import LocalCache
from . import ServerUtil

CacheServer = None


class CacheSystem:
    def __init__(self, config, feeds=[]):
        self.feeds = feeds
        self.type = config['type'].lower()
        if self.type == 'redis':
            self.__cache = RedisCache.Cache(config)
        elif self.type == 'local':
            self.__cache = LocalCache.Cache(config)
        else:
            raise Exception('Unknown cache type [%s]' % self.type)
        self.__cache.set("__yogurt_test", "ping")
        ServerUtil.info('Cache setup [%s]' % self.type)

    def incubate(self):
        leagues = []
        for i in self.feeds:
            if hasattr(i, 'league'):
                leagues.append(i.league)
            feeds = filter(lambda x: x.startswith('Feed_'), dir(i))
            for y in feeds:
                getattr(i, y)()
        self.set('leagues', json.dumps({'leagues': leagues}))

    def get(self, key):
        return self.__cache.get(key)

    def set(self, key, value):
        ServerUtil.info('Cache setting key [%s] in [%s]' % (key, self.type))
        return self.__cache.set(key, value)

