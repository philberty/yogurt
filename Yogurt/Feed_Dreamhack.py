from . import FeedUtil
from . import Feed_TwitchTv

class Feeds_TwitchTv_Dreamhack:
    def __init__(self):
        self._filters = [
            'DreamHack Open: Moscow 2014',
            'DreamHack Open: Valencia 2014',
            'DreamHack Open: Summer 2014',
            'DreamHack Open 2014 Bucharest',
            #'DreamHack Open 2013 - Dreamhack Winter',
            #'DreamHack Open 2013 - DreamHack summer 2013',
            'DreamHack Winter 2012',
            'DHOpen summer',
            'Dreamhack Open Grand Finals',
            'DreamHack 2011'
        ]

    @property
    def league(self):
        return 'dreamhack'
        
    def _getTwitchDreamhackVdeos(self):
        videos = Feed_TwitchTv.getChannelVideos('dreamhacksc2', broadcasts=True)
        for i in Feed_TwitchTv.getChannelVideos('dreamhacksc2', broadcasts=False):
            videos.append(i)
        return videos

    @FeedUtil.CacheResult(timer=50)
    def getDreamhackVideos(self):
        videos = self._getTwitchDreamhackVdeos()
        sorted = {}
        for i in self._filters:
            sorted[i] = {'_type': 'list', '_keys': ['event']}
            sorted[i]['event'] = list(filter(lambda x: i in x['title'], videos))
        return sorted

    @FeedUtil.Feed(key='league/dreamhack', timer=60)
    def Feed_getDreamhackChannelInfo(self):
        return Feed_TwitchTv.getChannelObject('dreamhacksc2')

    @FeedUtil.Feed(key='league/dreamhack/events', timer=60)
    def Feed_getDreamhackEvents(self):
        videos = self.getDreamhackVideos()
        events = []
        for i in videos.keys():
            events.append(FeedUtil.restfiyString(i))
        return {'keys': events}

    @FeedUtil.Feed(base='league/dreamhack/event/%s', timer=60)
    def Feed_getDreamhackEventVideos(self):
        videos = self.getDreamhackVideos()
        leagues = {}
        for i in videos.keys():
            leagues[i] = {FeedUtil.restfiyString(i): videos[i]}
        return leagues

