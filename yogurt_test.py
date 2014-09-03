#!/usr/bin/env python3

import json
import unittest

from Yogurt import YogurtApp
from Yogurt import AppCache
from Yogurt import Feed_TwitchTv
from Yogurt import setupTestLoggingAndCache

class TestFeedTwitchGSL(unittest.TestCase):
    def setUp(self):
        setupTestLoggingAndCache()
        self.app = YogurtApp.app.test_client()
        self._codes = ['Code S', 'Code A']
        self._leagues = ['2014 GSL Season 3', '2014 GSL Season 1', '2014 GSL Season 2']
        with open('./videos.json', 'r') as fd:
            self._feedVideos = json.loads(fd.read())['videos']
        feed = Feed_TwitchTv.Feeds_TwitchTv_GSL()
        self.gsl = feed.getSortedGslBroadcasts(self._feedVideos)
        AppCache.CacheServer.set ('testLeagues', json.dumps(self.gsl))

    def testGslFeed(self):
        resp = self.app.get('/api/testLeagues')
        data = json.loads (resp.data.decode("utf-8"))
        assert data['status'] == 200
        ndata = {}
        for i in data.keys():
            if i != 'status':
                ndata[i] = data[i]
        for i in ndata.keys():
            assert i in self._leagues
            for j in self._codes:
                assert j in self.gsl[i]

if __name__ == '__main__':
    unittest.main()
