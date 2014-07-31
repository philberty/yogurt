#!/usr/bin/env python

import json
import unittest

import Yogurt
from Yogurt import ServerUtil
from Yogurt import AppCache
from Yogurt import FeedUtil
from Yogurt import YogurtApp

class TestFeed (object):
    @FeedUtil.Feed (key='test')
    def Feed_generateSomeData (self):
        return {'test':[1,2,3]}

class YogurtTestRestApi (unittest.TestCase):

    def setUp (self):
        Yogurt.SetupTestEnv ([TestFeed ()])
        YogurtApp.app.config ['TESTING'] = True
        self.app = YogurtApp.app.test_client ()

    def test_pass (self):
        resp = self.app.get ('/api/test')
        assert resp.status_code == 200
        r = json.loads (resp.data.decode("utf-8"))
        assert (r ['status'] == 200)
        print (r)

    def test_fail (self):
        resp = self.app.get ('/api/willfail')
        assert resp.status_code == 404
        r = json.loads (resp.data.decode("utf-8"))
        assert (r ['status'] == 404)
        print (r)

if __name__ == '__main__':
    unittest.main ()
