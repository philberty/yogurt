#!/usr/bin/env python

import os
import sys
import logging
import optparse
import traceback
import logging.config

import Yogurt

from Yogurt import feed_youtube
from ConfigParser import RawConfigParser as CParser

def printVersion ():
    print "Yogurt Feeder Version [%s]" % Yogurt.version

def serverMain ():
    global _spid, _rpid
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
        print >> sys.stderr, "Error requires config file see --help"
        sys.exit (1)
    try:
        parseConfig = CParser ()
        parseConfig.read (options.config)
        cache = str (parseConfig.get ("yogurt", "cache"))
        cache_config = parseConfig._sections [cache]
    except:
        print >> sys.stderr, "Error Parsing config [%s]" % sys.exc_info ()[1]
        sys.exit (1)
    timer = None
    try:
        timer = int (parseConfig.get ("feeder", "timer"))
    except:
        pass
    feed_config = None
    try:
        import Yogurt.FeedConfig as fc
        feed_config = fc.__feed_config
    except IOError:
        print >> sys.stderr, "FeedConfig unavailable! Yogurt.FeedConfig.py"
        sys.exit (1)
    try:
        feed_youtube.__key = parseConfig._sections ['feed_youtube']['key']
    except:
        pass
    logging.config.fileConfig (options.config)
    if options.fork is True:
        pid = os.fork ()
        if pid == -1:
            print >> sys.stderr, "Error forking as daemon"
            sys.exit (1)
        elif pid == 0:
            os.setsid ()
            os.umask (0)
        else:
            print pid
            sys.exit (0)
    Yogurt.YogurtFeeder (feed_config, cache_config).run (timer)

if __name__ == "__main__":
    serverMain ()
