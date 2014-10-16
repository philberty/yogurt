import requests

from . import ServerUtil


def getChannelVideos(channel, broadcasts=True, offset=50):
    videos = []
    _endPoint = 'https://api.twitch.tv/kraken'
    _channelPath = '/channels/%s/videos'
    headers = {'Accept': 'application/vnd.twitchtv.v2+json'}
    payload = {'broadcasts': str(broadcasts).lower(), 'limit': offset, 'offset': 0}
    while True:
        ServerUtil.debug("Twitch Channel [%s] videos offset [%s]"
                        % (channel, payload['offset']))
        resp = requests.get(_endPoint + (_channelPath % channel), params=payload, headers=headers)
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
