#!/usr/bin/env python3

import json
import unittest

from Yogurt import Feed_TwitchTv
from Yogurt import setupTestLoggingAndCache

class TestFeedTwitchGSL(unittest.TestCase):
    def setUp(self):
        setupTestLoggingAndCache()
        self._codes = ['Code S', 'Code A']
        self._leagues = ['2014 GSL Season 3', '2014 GSL Season 1', '2014 GSL Season 2']
        with open('./videos.json', 'r') as fd:
            self._feedVideos = json.loads(fd.read())['videos']

    def testGslFeed(self):
        feed = Feed_TwitchTv.Feeds_TwitchTv_GSL()
        gsl = feed.getSortedGslBroadcasts(self._feedVideos)
        for i in gsl.keys():
            assert i in self._leagues
            for j in self._codes:
                assert j in gsl[i]
        for i in gsl[self._leagues[2]][self._codes[0]]:
            print(gsl[self._leagues[2]][self._codes[0]][i].keys())


if __name__ == '__main__':
    unittest.main()
