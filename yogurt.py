#!/usr/bin/env python

import os
import sys
import logging
import optparse
import traceback
import logging.config

import Yogurt
from Yogurt import feed_youtube
from Yogurt import feed_teamliquid
from configparser import RawConfigParser as CParser

def printVersion ():
    print ("Yogurt Version [%s]" % Yogurt.version)

def serverMain ():
    parser = optparse.OptionParser ()
    parser.add_option ("-v", "--version", dest='version',
                       help="Print version", action="store_true")
    parser.add_option ("-c", "--config", dest="config",
                       help="Config file location", default=None)
    parser.add_option ("-F", "--fork", dest="fork", action="store_true",
                       help="Fork as daemon", default=False)
    (options, args) = parser.parse_args ()
    if options.version is True:
        printVersion ()
        return
    if options.config is None:
        sys.exit ( "Error requires config file see --help")
    try:
        parseConfig = CParser ()
        parseConfig.read (options.config)
        wbind = str (parseConfig.get ("yogurt", "web_bind"))
        wport = int (parseConfig.get ("yogurt", "web_port"))
        cache = str (parseConfig.get ("yogurt", "cache"))
        cache_config = parseConfig._sections [cache]
    except:
        sys.exit ("Error Parsing config [%s]" % sys.exc_info ()[1])
    logging.config.fileConfig (options.config)
    if options.fork is True:
        pid = os.fork ()
        if pid == -1:
            sys.exit ("Error forking as daemon")
        elif pid == 0:
            os.setsid ()
            os.umask (0)
        else:
            print (pid)
            sys.exit (0)
    feeds = [feed_teamliquid.FeedTeamLiqud ()]
    Yogurt.YogurtServer (wbind, wport, cache_config, feeds).listen ()

if __name__ == "__main__":
    serverMain ()
