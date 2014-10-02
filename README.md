# FringeTV

[![Build Status](https://travis-ci.org/redbrain/yogurt.svg?branch=master)](https://travis-ci.org/redbrain/yogurt)

FringeTV is a feed aggregator for eSports. Feed handlers scrape set sites and push JSON representations of available VoD's, live streams and  upcomming events into Redis cache.

![FringeTV](/Yogurt/www/img/screenshot.png?raw=true "FringeTV")

## Compilation and installation

Development on Mac:

```bash
# get Python 3 - redis and node + npm
$ brew install npm python3 redis
# install python dependancies
$ sudo pip3 install -r requirements.txt
# install bower to get javascript dependancies
$ sudo npm install -g bower
# install javascript deps
$ bower install

# run server unit-tests
$ python3 ./yogurt_test.py
```

Then in seperate bash shells run:

```bash
# run the data-store
$ redis-server
# run the feed-handlers
$ ./feeder.py -c etc/yogurt/yogurt.cfg # fills your cache with data
# run the webapp
$ ./yogurt.py -c etc/yogurt/yogurt.cfg # runs the webapp
```

The Feeder process run's constantly filling the cache constantly you can stop it at any time but you won't get
automatic updates.

The webapp is run and in Production it is behind a nginx reverse proxy configuration.

