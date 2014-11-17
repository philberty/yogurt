from . import FeedUtil
from . import Feed_TwitchTv

class Feeds_TwitchTv_TakeTv:
    def __init__(self):
        self._filters = [
            'HomeStoryCup VI',
            'HomeStoryCup VII',
            'HomeStory Cup IX',
            'HomeStory Cup X'
        ]

    @property
    def league(self):
        return 'taketv'

    @FeedUtil.CacheResult(timer=50)
    def getTakeTvVideos(self):
        videos = Feed_TwitchTv.getChannelVideos('taketv')
        sorted = {}
        for i in self._filters:
            sorted[i] = {'_type': 'list', '_keys': ['event']}
            sorted[i]['event'] = list(filter(lambda x: i in x['title'], videos))
        return sorted

    @FeedUtil.Feed(key='league/taketv', timer=60)
    def Feed_getTakeTvChannelInfo(self):
        return Feed_TwitchTv.getChannelObject('taketv')

    @FeedUtil.Feed(key='league/taketv/events', timer=60)
    def Feed_getTakeTvEvents(self):
        videos = self.getTakeTvVideos()
        events = []
        for i in videos.keys():
            events.append(FeedUtil.restfiyString(i))
        return {'keys': events}

    @FeedUtil.Feed(base='league/taketv/event/%s', timer=60)
    def Feed_getWcseuEventVideos(self):
        videos = self.getTakeTvVideos()
        leagues = {}
        for i in videos.keys():
            leagues[i] = {FeedUtil.restfiyString(i): videos[i]}
        return leagues

