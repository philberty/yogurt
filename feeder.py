#!/usr/bin/env python3

import os
import sys
import imp
import logging
import optparse
import logging.config

from Yogurt import Feed_GSL
from Yogurt import Feed_Redbull
from Yogurt import Feed_Dreamhack
from Yogurt import Feed_TeamLiquid
from Yogurt import Feed_WCS_EU
from Yogurt import Feed_WCS_USA
from Yogurt import Feed_TakeTv

from Yogurt import Feeder


def get_cache_config(filename):
    d = imp.new_module('config')
    d.__file__ = filename
    try:
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
    except IOError as e:
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
    return d.__dict__['APP_CACHE']


def main ():
    parser = optparse.OptionParser ()
    parser.add_option("-c", "--config", dest="config",
                      help="Config file location", default=None)
    (options, args) = parser.parse_args()
    if options.config is None:
        sys.exit("Error requires config file see --help")
    cache_config = get_cache_config(options.config)
    feeds = [
        Feed_TeamLiquid.Feeds_TeamLiquid(),
        Feed_Dreamhack.Feeds_TwitchTv_Dreamhack(),
        Feed_Redbull.Feeds_TwitchTv_RedBull(),
        Feed_GSL.Feeds_TwitchTv_GSL(),
        Feed_WCS_EU.Feeds_TwitchTv_WCS_Europe(),
        Feed_WCS_USA.Feeds_TwitchTv_WCS_USA(),
        Feed_TakeTv.Feeds_TwitchTv_TakeTv()
    ]
    Feeder.Feeder(cache_config, feeds).run()

if __name__ == "__main__":
    main()
