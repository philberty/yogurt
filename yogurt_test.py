#!/usr/bin/env python3

import json
import unittest

import Yogurt

from Yogurt import AppCache
AppCache.Testing = True

from Yogurt import FeedUtil
from Yogurt import YogurtApp

from Yogurt import Feed_GSL
from Yogurt import Feed_Redbull
from Yogurt import Feed_TwitchTv
from Yogurt import Feed_Dreamhack

from unittest.mock import MagicMock

class MockFeedClass(object):
    @FeedUtil.Feed(key='mock', timer=60)
    def Feed_mockFeed(self):
        return {'mock': 'mock'}

class TestApi_Mock(unittest.TestCase):
    def setUp(self):
        cache = Yogurt.testingResetCache()
        self.app = YogurtApp.app.test_client()
        cache.injectFeed(MockFeedClass())
        cache.incubate()

    def testMockFeed(self):
        resp = self.app.get('/api/mock')
        payload = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(resp.status, '200 OK')

    def testWrongApiFailsWithNotFound(self):
        resp = self.app.get('/wrong')
        self.assertEqual(resp.status, '404 NOT FOUND')

class TestFeedTwitch_Dreamhack(unittest.TestCase):
    def setUp(self):
        cache = Yogurt.testingResetCache()
        self.app = YogurtApp.app.test_client()
        with open('tests/DreamhackTestData.json', 'r') as fd:
            videos = json.loads(fd.read())['videos']
            Feed_TwitchTv.getChannelVideos = MagicMock(return_value=videos)
            Feed_TwitchTv.getChannelObject = MagicMock(return_value={})
        cache.injectFeed(Feed_Dreamhack.Feeds_TwitchTv_Dreamhack())
        cache.incubate()

    def testGetListOfLeagues(self):
        resp = self.app.get('/api/leagues')
        payload = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(len(payload['leagues']), 1)
        self.assertTrue('dreamhack' in payload['leagues'])

    def testGetMockDHLeagueObject(self):
        resp = self.app.get('/api/league/dreamhack')
        self.assertEqual(resp.status, '200 OK')

    def testGetMockDHLeagueEventList(self):
        resp = self.app.get('/api/league/dreamhack/events')
        payload = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(len(payload['keys']), 9)

    def testGetMockDHLeagueEventObject(self):
        resp = self.app.get('/api/league/dreamhack/event/DreamHackOpenValencia2014')
        payload = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(resp.status, '200 OK')

class TestFeedTwitch_GSL(unittest.TestCase):
    def setUp(self):
        cache = Yogurt.testingResetCache()
        self.app = YogurtApp.app.test_client()
        with open('tests/GslTestData.json', 'r') as fd:
            videos = json.loads(fd.read())['videos']
            Feed_TwitchTv.getChannelVideos = MagicMock(return_value=videos)
            Feed_TwitchTv.getChannelObject = MagicMock(return_value={})
        cache.injectFeed(Feed_GSL.Feeds_TwitchTv_GSL())
        cache.incubate()

    def testGetListOfLeagues(self):
        resp = self.app.get('/api/leagues')
        payload = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(resp.status, '200 OK')
        self.assertTrue('gsl' in payload['leagues'])

    def testGetMockGslLeagueObject(self):
        resp = self.app.get('/api/league/gsl')
        self.assertEqual(resp.status, '200 OK')

    def testGetMockGSLLeagueEventList(self):
        resp = self.app.get('/api/league/gsl/events')
        payload = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(len(payload['keys']), 3)

    def testGetMockGSLLeagueEventObject(self):
        resp = self.app.get('/api/league/gsl/event/2014GSLSeason2')
        payload = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(resp.status, '200 OK')
        with open('listing.json', 'w') as fd:
            fd.write(json.dumps(payload, indent=4))

if __name__ == '__main__':
    unittest.main(verbosity=2)
