#!/usr/bin/env python3

import os
import sys
import logging
import optparse
import logging.config

import Yogurt
from Yogurt import Feed_TwitchTv
from Yogurt import Feed_TeamLiquid
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
        sys.exit("Error Parsing config [%s]" % sys.exc_info ()[1])
    logging.config.fileConfig(options.config)
    if options.fork is True:
        pid = os.fork()
        if pid == -1:
            sys.exit("error Demonizing!")
        elif pid == 0:
            os.setsid()
            os.umask(0)
        else:
            print(pid)
            sys.exit(0)
    feeds = [
        Feed_TeamLiquid.Feeds_TeamLiquid(),
        Feed_TwitchTv.Feeds_TwitchTv_GSL(),
        Feed_TwitchTv.Feeds_TwitchTv_Dreamhack(),
        Feed_TwitchTv.Feeds_TwitchTv_RedBull()
    ]
    Yogurt.YogurtFeeder(cache_config, feeds).run()

if __name__ == "__main__":
    serverMain ()
