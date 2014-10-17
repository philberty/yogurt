import requests

from . import ServerUtil

from pyquery import PyQuery as pq

def getBracketEmbedCodeFromURL(url):
    ServerUtil.info('Trying to fetch bracket [%s]' % url)
    request = requests.get(url)
    if not request.ok:
        return
    dom = pq(request.content)
    elem = dom('#Embed').find('textarea')[0]
    return elem.value.trim()
