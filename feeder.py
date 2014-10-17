#!/usr/bin/env python3

import os
import sys
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

from Yogurt import YogurtFeeder

from configparser import RawConfigParser as CParser

def serverMain ():
    parser = optparse.OptionParser ()
    parser.add_option("-c", "--config", dest="config",
                      help="Config file location", default=None)
    (options, args) = parser.parse_args()
    if options.config is None:
        sys.exit("Error requires config file see --help")
    try:
        parseConfig = CParser()
        parseConfig.read(options.config)
        cache = str (parseConfig.get("yogurt", "cache"))
        cache_config = parseConfig._sections[cache]
    except:
        sys.exit("Error Parsing config [%s]" % (options.config, sys.exc_info ()[1]))
    logging.config.fileConfig(options.config)
    feeds = [
        Feed_TeamLiquid.Feeds_TeamLiquid(),
        Feed_Dreamhack.Feeds_TwitchTv_Dreamhack(),
        Feed_Redbull.Feeds_TwitchTv_RedBull(),
        Feed_GSL.Feeds_TwitchTv_GSL(),
        Feed_WCS_EU.Feeds_TwitchTv_WCS_Europe(),
        Feed_WCS_USA.Feeds_TwitchTv_WCS_USA(),
        Feed_TakeTv.Feeds_TwitchTv_TakeTv()
    ]
    YogurtFeeder(cache_config, feeds).run()

if __name__ == "__main__":
    serverMain ()
