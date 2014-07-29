#!/usr/bin/env python

import json
import unittest

from Yogurt import AppCache
from Yogurt import YogurtApp as FlaskApp

def GenerateCacheData ():
    return {'foo':1, 'bar':[1,2,3,4]}

def PrintJsonPretty (data):
    print json.dumps (data, indent=4, separators=(',', ': '))

class YogurtTestRestApi (unittest.TestCase):
    def setUp (self):
        FlaskApp.app.config ['TESTING'] = True
        self.app = FlaskApp.app.test_client()
        feed_config = [{'key':'test', 'hook':GenerateCacheData}]
        AppCache.CacheServer = AppCache.CacheSystem ('shelve', { },
                                                     feed_config={'timeout':-1,
                                                                  'feeds':feed_config
                                                              })
    
    def tearDown (self):
        pass

    def test_pass (self):
        resp = self.app.get ('/api/test')
        assert resp.status_code == 200
        data = json.loads (resp.data)
        PrintJsonPretty (data)

    def test_fail (self):
        resp = self.app.get ('/api/willfail')
        assert resp.status_code == 404
        data = json.loads (resp.data)
        PrintJsonPretty (data)

if __name__ == '__main__':
    unittest.main ()
