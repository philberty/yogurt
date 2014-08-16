import re
import sys
import requests

from . import FeedUtil
from . import ServerUtil


def getChannelVideos(channel, broadcasts=False, offset=40):
        """

        :param channel: The channel name on Twitch.tv
        :return: A List of all videos
        """
        videos = []
        _endPoint = 'https://api.twitch.tv/kraken'
        _channelPath = '/channels/%s/videos'
        params = {'broadcasts': broadcasts, 'limit': offset, 'offset': 0}
        while True:
            ServerUtil.info("Twitch Channel [%s] videos offset [%s]"
                            % (channel, params['offset']))
            resp = requests.get(_endPoint + (_channelPath % channel), params=params)
            if not resp.ok:
                raise Exception('Unable to fetch url [%s]', resp)
            data = resp.json()
            if len(data['videos']) == 0:
                break
            else:
                for video in data['videos']:
                    videos.append(video)
            params['offset'] += offset
        return videos



class Feeds_TwitchTv_GSL(object):
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
        sorted = {'Code S': [], 'Code A': []}
        for video in videos:
            for code in sorted.keys():
                if code in video['title']:
                    sorted[code].append(video)
        return sorted

    def sortGslVideosByRound(self, videos):
        ServerUtil.info('Sort League Code by Rounds')
        sorted = {}
        for i in videos:
            try:
                round = re.search('Ro[0-9][0-9].', i['title'])
                if round is None:
                    round = re.search('Ro[0-9].', i['title'])
                    if round is None:
                        round = re.search('Final', i['title'])
                round = round.group()
                if not round in sorted:
                    sorted[round] = []
                sorted[round].append(i)
            except:
                pass
        return sorted

    def sortGslVideosByMatch(self, videos):
        ServerUtil.info('Sort Round by Matches')
        sorted = {}
        for i in videos:
            match = re.search('Match.[0-9]', i['title'])
            if match is None:
                match = re.search('Match[0-9]', i['title'])

            match = match.group()
            if not match in sorted:
                sorted[match] = []
            sorted[match].append(i)
        return sorted

    def getSortedGslBroadcasts(self, videos):
        allGslLeagues = self.sortGslVideosByLeague(videos)
        gslLeaguesSorted = {}
        for i in allGslLeagues.keys():
            sortedByCode = self.sortGslLeagueVideosByCode(allGslLeagues[i])
            sortedByCodeByRound = {}
            for j in sortedByCode.keys():
                sortedRound = self.sortGslVideosByRound(sortedByCode[j])
                for k in sortedRound.keys():
                    if k == 'Final':
                        sortedRound[k] = {'Final': sortedRound[k]}
                    else:
                        sortedRound[k] = self.sortGslVideosByMatch(sortedRound[k])
                sortedByCodeByRound[j] = sortedRound
            gslLeaguesSorted[i] = sortedByCodeByRound
        return gslLeaguesSorted

    @FeedUtil.CacheResult(timer=50)
    def getGslVideos(self):
        #videos = getChannelVideos('gsl', broadcasts=True)
        #return self.getSortedGslBroadcasts(videos)
        with open('videos.json', 'r') as fd:
            import json
            videos = json.loads(fd.read())['videos']
            return self.getSortedGslBroadcasts(videos)

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
            leagues[i] = gsl[i]
        return leagues
