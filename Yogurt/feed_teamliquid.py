import sys

import re
import json
import requests
import ServerUtil

from pyquery import PyQuery as pq
from FeedUtil import FeedException, Feed

class FeedTeamLiqud:
    def __init__ (self):
        self.__base = 'http://teamliquid.net'

    def __parseEventInfo (self, node):
        elem = node.find_class ('rightmenu upcoming_text')
        data = elem [0].attrib
        ServerUtil.info ('Found event [%s]' % data ['title'])
        rhref = self.__base + data ['href']
        return {'event':rhref, 'title':data ['title']}

    def __parseStreamLink (self, stream):
        if 'twitch.tv' in stream:
            if 'twitch.tv/embed?channel' not in stream:
                channel = stream.split ('/').pop ()
                stream = "http://www.twitch.tv/embed?channel=" + channel
        elif 'teamliquid.net/video/streams' in stream:
            stream = self.__parseStreamTeamLiquid ({'href':stream})
        return stream

    def __parseStreamTeamLiquid (self, node):
        resp = requests.get (node ['href'])
        if not resp.ok:
            raise FeedException ('unable to fetch [%s]' % node ['href'])
        dom = pq (resp.content)
        try:
            stream = dom ('iframe.videoplayer').eq (0) [0]
            stream = stream.attrib ['src']
        except:
            stream = None
            ServerUtil.warning ('Unable to parse out stream info for [%s]' % node ['href'])
        finally:
            node ['stream'] = stream
        return node

    def __parseLiveStream (self, node):
        ServerUtil.info ('Looking up stream info [%s]' % node ['href'])
        if 'teamliquid.net/video/streams' in node ['href']:
            return self.__parseStreamTeamLiquid (node)
        else:
            ServerUtil.warning ('unknown stream location [%s]' % node ['href'])

    def __parseEventStreamInfo (self, node):
        ServerUtil.info ('Looking up event info for [%s]' % node ['title'])
        tag = node ['event'].split ('/').pop () [1:]
        resp = requests.get (node ['event'])
        if not resp.ok:
            raise FeedException ('Unable to fetch event info [%s]' % node ['event'])
        dom = pq (resp.content)
        element = dom ('a[name=\"%s\"]' % tag).eq (0)
        div = element.next ()
        elems = div.find ('td').eq (0)
        node ['description'] = elems.find ('div').text ()
        try:
            ilink = elems.find ('span').eq (0).find ('a').eq (0)[0].attrib ['href']
        except:
            ilink = None
        finally:
            node ['wiki_link'] = ilink
        links = []
        for i in elems.find ('a'):
            link = i.attrib ['href']
            if link [0] == '/':
                link = self.__base + link
            links.append (link)
        node ['links'] = links
        data = div.text ()
        try:
            stream = re.split ('Stream:', data)[1].strip ().split (' ')[0]
            stream = self.__parseStreamLink (stream)
        except:
            stream = None
        finally:
            node ['stream'] = stream
        try:
            thread = None
            if links [len (links) - 1] != node ['stream']:
                thread = links [len (links) - 1]
        except:
            pass
        finally:
            node ['thread'] = thread
        return node

    @Feed (key='live')
    def Feed_getLiveEvents (self):
        ServerUtil.info ('Looking for live events on teamliquid!')
        request = requests.get (self.__base)
        if not request.ok:
            raise FeedException ('unable to fetch [%s]' % self.__base)
        dom = pq (request.content)
        devents = dom ('div#calendar_content').eq (0).find ('strong')
        events = []
        for i in devents:
            node = i.find ('a')
            if node is None:
                continue
            link = node.attrib ['href']
            if link [0] == '/':
                link = self.__base + link
            events.append ({'title':node.attrib ['title'], 'event':link})
        events = map (self.__parseEventStreamInfo, events)
        return {'live_events':events, 'length':len (events)}

    @Feed (key='streams')
    def Feed_getStarcraftPlayerStreams (self):
        ServerUtil.info ('Looking for player streams on teamliquid!')
        request = requests.get (self.__base)
        if not request.ok:
            raise FeedException ('unable to fetch [%s]' % self.__base)
        dom = pq (request.content)
        streams_dom = dom ('div#streams_content').find ('div').eq (0).find ('a')
        streams = []
        for i in streams_dom:
            link = i.attrib ['href']
            if link [0] == '/':
                link = self.__base + link
            streams.append ({'name':i.text, 'href':link})
        streams = map (self.__parseLiveStream, streams)
        return {'starcraft2':streams, 'length':len (streams)}

    @Feed (key='upcoming')
    def Feed_getUpcomingEvents (self):
        ServerUtil.info ('Looking for upcomming events on teamliquid!')
        request = requests.get (self.__base)
        if not request.ok:
            raise FeedException ('unable to fetch [%s]' % self.__base)
        dom = pq (request.content)
        events = map (self.__parseEventInfo, dom ('table.upcoming').children ())
        events = map (self.__parseEventStreamInfo, events)
        return {'events':events, 'length':len (events)}
