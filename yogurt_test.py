#!/usr/bin/env python3

import json
import unittest

from Yogurt import AppCache
from Yogurt import FeedUtil
from Yogurt import YogurtApp
from Yogurt import Feed_TwitchTv
from Yogurt import setupTestEnviroment

from unittest.mock import MagicMock

class MockFeedClass(object):
    @FeedUtil.Feed(key='mock', timer=60)
    def Feed_mockFeed(self):
        return {'mock': 'mock'}

class TestFeedTwitchGSL(unittest.TestCase):
    def setUp(self):
        cache = setupTestEnviroment()
        self.app = YogurtApp.app.test_client()
        with open('videos.json', 'r') as fd:
            videos = json.loads(fd.read())['videos']
            Feed_TwitchTv.getChannelVideos = MagicMock(return_value=videos)
            Feed_TwitchTv.getChannelObject = MagicMock(return_value={})
        cache.injectFeed(MockFeedClass())
        cache.injectFeed(Feed_TwitchTv.Feeds_TwitchTv_GSL())
        cache.injectFeed(Feed_TwitchTv.Feeds_TwitchTv_Dreamhack())
        cache.incubate()

    def testMockFeed(self):
        resp = self.app.get('/api/mock')
        payload = json.loads(resp.data.decode("utf-8"))
        assert resp.status == '200 OK'
        assert 'mock' in payload

    def testGetListOfLeagues(self):
        resp = self.app.get('/api/leagues')
        payload = json.loads(resp.data.decode("utf-8"))
        assert resp.status == '200 OK'
        assert len(payload['leagues']) == 2

    def testGetMockGslLeagueObject(self):
        resp = self.app.get('/api/league/gsl')
        assert resp.status == '200 OK'

    def testGetMockDHLeagueObject(self):
        resp = self.app.get('/api/league/dreamhack')
        assert resp.status == '200 OK'

    def testGetMockGSLLeagueEventList(self):
        resp = self.app.get('/api/league/gsl/events')
        payload = json.loads(resp.data.decode("utf-8"))
        assert resp.status == '200 OK'
        assert len(payload['keys']) == 3

    def testGetMockDHLeagueEventList(self):
        resp = self.app.get('/api/league/dreamhack/events')
        payload = json.loads(resp.data.decode("utf-8"))
        assert resp.status == '200 OK'
        assert len(payload['keys']) == 9

    def testGetMockGSLLeagueEventObject(self):
        resp = self.app.get('/api/league/gsl/event/2014GSLSeason3')
        assert resp.status == '200 OK'

    def testGetMockDHLeagueEventObject(self):
        resp = self.app.get('/api/league/dreamhack/event/DreamHackOpenValencia2014')
        assert resp.status == '200 OK'

if __name__ == '__main__':
    unittest.main(verbosity=2)
