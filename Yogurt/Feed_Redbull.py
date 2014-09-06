from . import FeedUtil
from . import Feed_TwitchTv

class Feeds_TwitchTv_RedBull:
    def __init__(self):
        self._filters = [
            'Battle Grounds Detroit',
            'Red Bull Battle Grounds Global',
            'Red Bull Battle Grounds, New York City'
        ]

    @property
    def league(self):
        return 'redbull'

    @FeedUtil.CacheResult(timer=50)
    def getRedbullVideos(self):
        videos = Feed_TwitchTv.getChannelVideos('redbullesports')
        sorted = {}
        for i in self._filters:
            sorted[i] = {'_type': 'list', '_keys': ['event']}
            sorted[i]['event'] = list(filter(lambda x: i in x['title'], videos))
        return sorted

    @FeedUtil.Feed(key='league/redbull', timer=60)
    def Feed_getRedbullChannelInfo(self):
        return Feed_TwitchTv.getChannelObject('redbullesports')

    @FeedUtil.Feed(key='league/redbull/events', timer=60)
    def Feed_getRedbullEvents(self):
        videos = self.getRedbullVideos()
        events = []
        for i in videos.keys():
            events.append(FeedUtil.restfiyString(i))
        return {'keys': events}

    @FeedUtil.Feed(base='league/redbull/event/%s', timer=60)
    def Feed_getRedbullEventVideos(self):
        videos = self.getRedbullVideos()
        leagues = {}
        for i in videos.keys():
            leagues[i] = {FeedUtil.restfiyString(i): videos[i]}
        return leagues
