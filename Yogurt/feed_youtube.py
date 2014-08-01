import sys
import json
import requests

from . import ServerUtil
from . import FeedUtil

class FeedYouTube (object):
    def __init__ (self, url, key):
        self.url = url
        self.key = key

