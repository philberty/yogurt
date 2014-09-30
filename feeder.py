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

from Yogurt import YogurtFeeder

from configparser import RawConfigParser as CParser

def serverMain ():
    parser = optparse.OptionParser ()
    parser.add_option("-c", "--config", dest="config",
                      help="Config file location", default=None)
    parser.add_option("-F", "--fork", dest="fork", action="store_true",
                      help="Fork as daemon", default=False)
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
        Feed_GSL.Feeds_TwitchTv_GSL()
    ]
    YogurtFeeder(cache_config, feeds).run()

if __name__ == "__main__":
    serverMain ()
