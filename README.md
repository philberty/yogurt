# FringeTv

[![Build Status](https://travis-ci.org/redbrain/yogurt.svg?branch=master)](https://travis-ci.org/redbrain/yogurt)

Feed Aggregator for E-Sports FeedHandlers scrape Sites and push json representations of the VoD's and Events into
Redis Cache.

## Compilation and installation

Development on Mac:

```bash
$ brew install npm python3 redis
$ sudo pip3 install -r requirements.txt
$ sudo npm install -g bower
$ bower install

$ python3 ./yogurt_test.py
```

Then in seperate bash shells run:

```bash
$ redis-server
$ ./feeder.py -c etc/yogurt/yogurt.cfg # fills your cache with data
$ ./yogurt.py -c etc/yogurt/yogurt.cfg # runs the webapp
```

The Feeder process run's constantly filling the cache constantly you can stop it at any time but you won't get
automatic updates.

The webapp is run and in Production it is behind a nginx reverse proxy configuration.

