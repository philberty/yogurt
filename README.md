# FringeTv

[![Build Status](https://travis-ci.org/redbrain/yogurt.svg?branch=master)](https://travis-ci.org/redbrain/yogurt)

Feed Aggregator for E-Sports FeedHandlers scrape Sites and push json representations of the VoD's and Events into
Redis Cache.

## Compilation and installation

Development on Mac:

```bash
$ brew install npm python3
$ pip3 install requirements.txt
$ bower install

$ python3 ./yogurt_test.py

$ ./feeder.py -c etc/yogurt/yogurt.cfg # fills your specified cache 
$ ./yogurt.py -c etc/yogurt/yogurt.cfg # runs the webapp
```

