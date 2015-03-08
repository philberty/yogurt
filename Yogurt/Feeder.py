from . import AppCache
from . import ServerUtil

class Feeder:
    def __init__(self, cache_config, feeds):
        AppCache.CacheServer = AppCache.CacheSystem(cache_config, feeds=feeds)

    def run(self):
        ServerUtil.info('Feeding...')
        try:
            AppCache.CacheServer.incubate()
        except KeyboardInterrupt:
            ServerUtil.info('Caught Keyboard interrupt stopping!')
