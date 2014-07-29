import sys
import json
import requests
import ServerUtil

from FeedUtil import FeedException, Feed
from ConfigParser import RawConfigParser as CParser

class FeedYouTube (object):
    def __init__ (self, url, key):
        self.url = url
        self.key = key

