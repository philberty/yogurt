import re
import sys
import requests

from . import FeedUtil
from . import ServerUtil


def getChannelVideos(channel, broadcasts=True, offset=50):
    videos = []
    _endPoint = 'https://api.twitch.tv/kraken'
    _channelPath = '/channels/%s/videos'
    payload = {'broadcasts': str(broadcasts).lower(), 'limit': offset, 'offset': 0}
    while True:
        ServerUtil.info("Twitch Channel [%s] videos offset [%s]"
                        % (channel, payload['offset']))
        resp = requests.get(_endPoint + (_channelPath % channel), params=payload)
        if not resp.ok:
            raise Exception('Unable to fetch url [%s]', resp)
        data = resp.json()
        if len(data['videos']) == 0:
            break
        else:
            for video in data['videos']:
                videos.append(video)
        payload['offset'] += offset
    return videos


def getChannelObject(channel):
    ServerUtil.info("Fetching Twitch Tv Channel object for [%s]" % channel)
    _endPoint = 'https://api.twitch.tv/kraken'
    _channelPath = '/channels/%s'
    resp = requests.get(_endPoint + (_channelPath % channel))
    if not resp.ok:
        raise Exception('Unable to fetch url [%s]', resp)
    return resp.json()
        

class Feeds_TwitchTv_Dreamhack:
    def __init__(self):
        self._filters = [
            'DreamHack Open: Valencia 2014',
            'DreamHack Open: Summer 2014',
            'DreamHack Open 2014 Bucharest',
            'DreamHack Open 2013 - Dreamhack Winter',
            'DreamHack Open 2013 - DreamHack summer 2013',
            'DreamHack Winter 2012',
            'DHOpen summer',
            'Dreamhack Open Grand Finals',
            'DreamHack 2011'
        ]

    @property
    def league(self):
        return 'dreamhack'
        
    def _getTwitchDreamhackVdeos(self):
        videos = getChannelVideos('dreamhacksc2', broadcasts=True)
        for i in getChannelVideos('dreamhacksc2', broadcasts=False):
            if i not in videos:
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
        return getChannelObject('dreamhacksc2')

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

class Feeds_TwitchTv_GSL(object):
    @property
    def league(self):
        return "gsl"

    def sortGslVideosByLeague(self, videos):
        ServerUtil.info('Sort Videos by League')
        leagues = {}
        for i in videos:
            try:
                league = i['title'].split(',')[1].split('.')[0].strip()
                if league not in leagues:
                    leagues[league] = []
                leagues[league].append (i)
            except:
                pass
        return leagues

    def sortGslLeagueVideosByCode(self, videos):
        ServerUtil.info('Sort League by Code A/S')
        sorted = {'CodeS': [], 'CodeA': []}
        codeKeys = ['Code S', 'Code A']
        for video in videos:
            for code in codeKeys:
                if code in video['title']:
                    sorted[FeedUtil.restfiyString(code)].append(video)
        return sorted

    def sortGslVideosByGroup(self, videos):
        ServerUtil.info('Sort League Code Round by Group')
        sorted = {}
        for i in videos:
            try:
                group = re.search('Group [a-zA-Z]', i['title'])
                if group is None:
                    group = re.search('Final', i['title'])
                group = FeedUtil.restfiyString(group.group())
                if group not in sorted:
                    sorted[group] = []
                sorted[group].append(i)
            except:
                pass
        return sorted

    def sortGslVideosByRound(self, videos):
        ServerUtil.info('Sort League Code by Rounds')
        sorted = {}
        for i in videos:
            try:
                round = re.search('Ro[0-9][0-9]', i['title'])
                if round is None:
                    round = re.search('Ro[0-9]', i['title'])
                    if round is None: 
                        round = re.search('Final', i['title'])
                round = FeedUtil.restfiyString(round.group())
                if round not in sorted:
                    sorted[round] = []
                sorted[round].append(i)
            except:
                pass
        return sorted

    def sortGslVideosByMatch(self, videos):
        ServerUtil.info('Sort Round by Matches')
        sorted = {}
        for i in videos:
            try:
                match = re.search('Match.[0-9]', i['title'])
                if match is None:
                    match = re.search('Match[0-9]', i['title'])
                    if match is None:
                        if 'Final' in i ['title']:
                            match = 'Final'
                match = FeedUtil.restfiyString(match.group())
                if not match in sorted:
                    sorted[match] = []
                sorted[FeedUtil.restfiyString(match)].append(i)
            except:
                pass
        return sorted

    def sortGslCodeAVideos(self, videos):
        sortedByGroup = self.sortGslVideosByGroup(videos)
        groupKeys = list(sortedByGroup.keys())
        groupKeys.sort()
        sortedByGroup['_type'] = 'dir'
        sortedByGroup['_keys'] = groupKeys
        for i in groupKeys:
            sortedByGroup[i] = self.sortGslVideosByMatch(sortedByGroup[i])
            listKeys = list(sortedByGroup[i].keys())
            listKeys.sort()
            sortedByGroup[i]['_type'] = 'list'
            sortedByGroup[i]['_keys'] = listKeys
        return sortedByGroup

    def sortGslCodeSVideos(self, videos):
        sortedByRound = self.sortGslVideosByRound(videos)
        roundKeys = list(sortedByRound.keys())
        roundKeys.sort()
        sortedByRound['_type'] = 'dir'
        sortedByRound['_keys'] = roundKeys
        for i in roundKeys:
            sortedByRound[i] = self.sortGslVideosByGroup(sortedByRound[i])
            groupKeys = list(sortedByRound[i].keys())
            groupKeys.sort()
            sortedByRound[i]['_type'] = 'dir'
            sortedByRound[i]['_keys'] = groupKeys
            for j in groupKeys:
                sortedByRound[i][j] = self.sortGslVideosByMatch(sortedByRound[i][j])
                listKeys = list(sortedByRound[i][j].keys())
                listKeys.sort()
                sortedByRound[i][j]['_type'] = 'list'
                sortedByRound[i][j]['_keys'] = listKeys
        return sortedByRound

    def getSortedGslBroadcasts(self, videos):
        allGslLeagues = self.sortGslVideosByLeague(videos)
        gslLeaguesSorted = {}
        for i in allGslLeagues.keys():
            league = FeedUtil.restfiyString(i)
            gslLeaguesSorted[league] = self.sortGslLeagueVideosByCode(allGslLeagues[i])
            codeKeys = list(gslLeaguesSorted[league].keys())
            gslLeaguesSorted[league]['_type'] = 'dir'
            gslLeaguesSorted[league]['_keys'] = codeKeys
            gslLeaguesSorted[league]['CodeA'] = self.sortGslCodeAVideos(gslLeaguesSorted[league]['CodeA'])
            gslLeaguesSorted[league]['CodeS'] = self.sortGslCodeSVideos(gslLeaguesSorted[league]['CodeS'])
        return gslLeaguesSorted

    @FeedUtil.CacheResult(timer=50)
    def getGslVideos(self):
        videos = getChannelVideos('gsl', broadcasts=True)
        return self.getSortedGslBroadcasts(videos)

    @FeedUtil.Feed(key='league/gsl', timer=60)
    def Feed_getGslChannelInfo(self):
        return getChannelObject('gsl')

    @FeedUtil.Feed(key='league/gsl/events', timer=60)
    def Feed_getGSLEvents(self):
        gsl = self.getGslVideos()
        events = []
        for i in gsl.keys():
            events.append(FeedUtil.restfiyString(i))
        return {'keys': events}

    @FeedUtil.Feed(base='league/gsl/event/%s', timer=60)
    def Feed_getGSLEventVideos(self):
        gsl = self.getGslVideos()
        leagues = {}
        for i in gsl.keys():
            leagues[i] = {FeedUtil.restfiyString(i): gsl[i]}
        return leagues
