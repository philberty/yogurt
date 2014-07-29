import sys
import logging

version = '0.2'

def __setup_testing_env ():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

def info (message): logging.info (message)

def debug (message): logging.debug (message)

def warning (message): logging.warning (message)

def error (message): logging.error (message)

def fatal (message, _exit=True):
    logging.fatal (message)
    if _exit is True:
        sys.exit (1)
