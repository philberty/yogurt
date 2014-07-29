import redis

class Cache:
    def __init__ (self, config):
        self.__cache = redis.StrictRedis (host = config ['host'],
                                          port = config ['port'],
                                          db=0)

    def get (self, key):
        return self.__cache.get (key)

    def set (self, key, value):
        return self.__cache.set (key, value)
