import json
import asyncio

from . import RedisCache
from . import LocalCache
from . import ServerUtil
from . import ShelveCache

Testing = False
CacheServer = None

class CacheSystem:
    def __init__(self, config, feeds=[]):
        self.feeds = feeds
        self.type = config['type'].lower()
        self.__cache = None
        if self.type == 'redis':
            self.__cache = RedisCache.Cache(config)
        elif self.type == 'shelve':
            self.__cache = ShelveCache.Cache(config)
        elif self.type == 'local':
            self.__cache = LocalCache.Cache(config)
        else:
            raise Exception('Unknown cache type [%s]' % self.type)
        self.__cache.set("__yogurt_test", "ping")
        ServerUtil.info('Cache setup [%s]' % self.type)

    def injectFeed(self, feed):
        self.feeds.append(feed)

    def _incubateLeagues(self):
        leagues = []
        for i in self.feeds:
            if hasattr(i, 'league'):
                leagues.append(i.league)
        self.set('leagues', json.dumps({'leagues': leagues}))

    def _incubateFeeds(self, feeds):
        for i in feeds:
            feed = i[0]
            for hook in i[1]:
                getattr(feed, hook)()

    def _incubateFeedsAsync(self, feeds):
        loop = asyncio.get_event_loop()
        for i in feeds:
            feed = i[0]
            for hook in i[1]:
                asyncio.async(getattr(feed, hook)())
        try:
            loop.run_forever()
        finally:
            loop.close()

    def incubate(self):
        self._incubateLeagues()
        feeds = []
        for i in self.feeds:
            hooks = filter(lambda x: x.startswith('Feed_'), dir(i))
            feeds.append((i, list(hooks)))
        incubateFeeds = self._incubateFeeds if Testing else self._incubateFeedsAsync
        incubateFeeds(feeds)

    def get(self, key):
        return self.__cache.get(key)

    def set(self, key, value):
        ServerUtil.info('Cache setting key [%s] in [%s]' % (key, self.type))
        return self.__cache.set(key, value)

