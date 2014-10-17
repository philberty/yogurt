from . import FeedUtil
from . import Feed_TwitchTv

class Feeds_TwitchTv_WCS_Europe:
    def __init__(self):
        self._filters = [
            'WCS Europe - Season 3',
            'WCS Europe - Season 2',
            'WCS Europe 2014 - Season 1 - Premier League'
        ]

    @property
    def league(self):
        return 'wcseurope'

    @FeedUtil.CacheResult(timer=50)
    def getWcseuVideos(self):
        videos = Feed_TwitchTv.getChannelVideos('wcs_europe')
        sorted = {}
        for i in self._filters:
            sorted[i] = {'_type': 'list', '_keys': ['event']}
            sorted[i]['event'] = list(filter(lambda x: i in x['title'], videos))
        return sorted

    @FeedUtil.Feed(key='league/wcseurope', timer=60)
    def Feed_getWcseuChannelInfo(self):
        return Feed_TwitchTv.getChannelObject('wcs_europe')

    @FeedUtil.Feed(key='league/wcseurope/events', timer=60)
    def Feed_getWcseuEvents(self):
        videos = self.getWcseuVideos()
        events = []
        for i in videos.keys():
            events.append(FeedUtil.restfiyString(i))
        return {'keys': events}

    @FeedUtil.Feed(base='league/wcseurope/event/%s', timer=60)
    def Feed_getWcseuEventVideos(self):
        videos = self.getWcseuVideos()
        leagues = {}
        for i in videos.keys():
            leagues[i] = {FeedUtil.restfiyString(i): videos[i]}
        return leagues
