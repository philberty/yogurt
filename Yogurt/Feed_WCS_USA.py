from . import FeedUtil
from . import Feed_TwitchTv

class Feeds_TwitchTv_WCS_USA:
    def __init__(self):
        self._filters = [
            'WCS America S2 Finals on NASL',
            'WCS America - Season 3',
            'WCS America - Season 2',
            'WCS America Season 1',
            'WCS America Challenger League',
            'WCS America S1 Premier League Finals'
        ]

    @property
    def league(self):
        return 'wcsamerica'

    @FeedUtil.CacheResult(timer=50)
    def getWcsusaVideos(self):
        videos = Feed_TwitchTv.getChannelVideos('wcs_america')
        sorted = {}
        for i in self._filters:
            sorted[i] = {'_type': 'list', '_keys': ['event']}
            sorted[i]['event'] = list(filter(lambda x: i in x['title'], videos))
        return sorted

    @FeedUtil.Feed(key='league/wcsamerica', timer=60)
    def Feed_getWcsusaChannelInfo(self):
        return Feed_TwitchTv.getChannelObject('wcs_america')

    @FeedUtil.Feed(key='league/wcsamerica/events', timer=60)
    def Feed_getWcsusaEvents(self):
        videos = self.getWcsusaVideos()
        events = []
        for i in videos.keys():
            events.append(FeedUtil.restfiyString(i))
        return {'keys': events}

    @FeedUtil.Feed(base='league/wcsamerica/event/%s', timer=60)
    def Feed_getWcsusaEventVideos(self):
        videos = self.getWcsusaVideos()
        leagues = {}
        for i in videos.keys():
            leagues[i] = {FeedUtil.restfiyString(i): videos[i]}
        return leagues
