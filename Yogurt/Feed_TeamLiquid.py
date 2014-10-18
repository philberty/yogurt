import re

from . import FeedUtil
from . import ServerUtil
from . import Feed_TwitchTv
from . import Feed_HitBoxTv
from . import Feed_BinaryBeast

import requests
from pyquery import PyQuery as pq


class Feeds_TeamLiquid:
    """
    This isn't very nice to read all of this code but there is no structured way to access these
    """

    def __init__(self):
        self.__base = 'http://corsproxy.com/teamliquid.net'

    def __parseEventInfo(self, node):
        elem = node.find_class('rightmenu upcoming_text')
        data = elem[0].attrib
        ServerUtil.info('Found event [%s]' % data['title'])
        rhref = self.__base + data['href']
        return {'event': rhref, 'title': data['title']}

    def __parseStreamLink(self, node):
        stream = node['href']
        if 'teamliquid.net/video/streams' in stream:
            return self.__parseStreamTeamLiquid(node)
        elif 'goodgame.ru' in stream:
            node['embed'] = stream
            return node
        elif 'hitbox.tv' in stream:
            channel = stream.split('/').pop()
            return self.__parseHitBoxTvStream(channel, node)
        elif 'twitch.tv' in stream:
            channel = stream.split('/').pop()
            if 'twitch.tv/embed' in stream:
                result = re.search("channel=[a-zA-Z0-9]*", stream)
                channel = result.group()
                channel = channel.split('=')[1]
            return self.__parseStreamTwitchTv(node, channel)

    def __parseHitBoxTvStream(self, channel, node):
        channelObject = Feed_HitBoxTv.getChannelObject(channel)
        node['object'] = channelObject
        node['name'] = channel
        channelStream = 'http://hitbox.tv/#!/embed/%s' % channel
        node['embed'] = "<iframe width=\"620\" height=\"378\" src=\"%s\" frameborder=\"0\" allowfullscreen></iframe>" % channelStream
        return node

    def __parseStreamTwitchTv(self, node, channel):
        channelObject = Feed_TwitchTv.getChannelObject(channel)
        node['followers'] = channelObject['followers']
        node['logo'] = channelObject['logo']
        node['views'] = channelObject['views']
        node['name'] = channel
        node['href'] = 'http://twitch.tv/%s' % channel
        channelStream = 'http://www.twitch.tv/%s/embed' % channel
        channelChat = 'http://twitch.tv/chat/embed?channel=%s&amp;popout_chat=true' % channel
        node['embed'] = "<iframe width=\"620\" height=\"378\" src=\"%s\" scrolling=\"0\" frameborder=\"0\"></iframe>" % channelStream
        node['embedChat'] = "<iframe frameborder=\"0\" scrolling=\"no\" id=\"chat_embed\" src=\"%s\" height=\"500\" width=\"350\"></iframe>" % channelChat
        return node

    def __parseStreamTeamLiquid(self, node):
        resp = requests.get(node['href'])
        if not resp.ok:
            raise Exception('unable to fetch [%s]' % node['href'])
        dom = pq(resp.content)
        try:
            stream = dom('iframe.videoplayer').eq(0)[0]
            stream = stream.attrib['src']
            node['href'] = stream
            return self.__parseStreamLink(node)
        except:
            stream = None
            ServerUtil.warning('Unable to parse out stream info for [%s]' % node['href'])
        return node

    def __parseBracket(self, links):
        for i in links:
            if 'binarybeast.com' in i:
                return Feed_BinaryBeast.getBracketEmbedCodeFromURL(i)

    def __parseEventStreamInfo(self, node):
        ServerUtil.info('Looking up event info for [%s]' % node['title'])
        tag = node['event'].split('/').pop()[1:]
        resp = requests.get(node['event'])
        if not resp.ok:
            raise Exception('Unable to fetch event info [%s]' % node['event'])
        dom = pq(resp.content)
        element = dom('a[name=\"%s\"]' % tag).eq(0)
        div = element.next()
        elems = div.find('td').eq(0)
        node['description'] = elems.find('div').text()
        try:
            ilink = elems.find('span').eq(0).find('a').eq(0)[0].attrib['href']
        except:
            ilink = None
        finally:
            node['wiki_link'] = ilink
        links = []
        for i in elems.find('a'):
            link = i.attrib['href']
            if link[0] == '/':
                link = self.__base + link
            links.append(link)
        node['links'] = links
        node['bracket'] = self.__parseBracket(links)
        data = div.text()
        try:
            stream = re.split('Stream:', data)[1].strip().split(' ')[0]
            stream = self.__parseStreamLink({'href': stream})
        except:
            stream = None
        finally:
            node['stream'] = stream
        try:
            thread = None
            if links[len(links) - 1] != node['stream']:
                thread = links[len(links) - 1]
        except:
            pass
        finally:
            node['thread'] = thread
        return node

    @FeedUtil.Feed(key='live', timer=30)
    def Feed_getLiveEvents(self):
        ServerUtil.info('Looking for live events on teamliquid!')
        request = requests.get(self.__base)
        if not request.ok:
            raise Exception('unable to fetch [%s]' % self.__base)
        dom = pq(request.content)
        devents = dom('div#calendar_content').eq(0).find('strong')
        events = []
        for i in devents:
            node = i.find('a')
            if node is None:
                continue
            link = node.attrib['href']
            link = self.__base + link
            eid = link.split('/').pop()
            events.append({'title': node.attrib['title'], 'event': link, 'id': eid[1:]})
        events = list(map(self.__parseEventStreamInfo, events))
        return {'live_events': events, 'length': len(events)}

    @FeedUtil.Feed(key='streams', timer=15)
    def Feed_getStarcraftPlayerStreams(self):
        ServerUtil.info('Looking for player streams on teamliquid!')
        request = requests.get(self.__base)
        if not request.ok:
            raise Exception('unable to fetch [%s]' % self.__base)
        dom = pq(request.content)
        streams_dom = dom('div#streams_content').find('div').eq(0).find('a')
        streams = []
        for i in streams_dom:
            link = i.attrib['href']
            if link[0] == '/':
                link = self.__base + link
            streams.append({'name': i.text, 'href': link})
        streams = list(map(self.__parseStreamLink, streams))
        return {'starcraft2': streams, 'length': len(streams)}

    @FeedUtil.Feed(key='upcoming', timer=100)
    def Feed_getUpcomingEvents(self):
        ServerUtil.info('Looking for upcomming events on teamliquid!')
        request = requests.get(self.__base)
        if not request.ok:
            raise Exception('unable to fetch [%s]' % self.__base)
        dom = pq(request.content)
        events = list(map(self.__parseEventInfo, dom('table.upcoming').children()))
        events = list(map(self.__parseEventStreamInfo, events))
        return {'events': events, 'length': len(events)}
