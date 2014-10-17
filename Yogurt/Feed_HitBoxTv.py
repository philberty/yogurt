import requests

from . import ServerUtil

def getChannelObject(channel):
    resp = requests.get('http://api.hitbox.tv/user/%s' % channel)
    if not resp.ok:
        return
    return resp.json()
