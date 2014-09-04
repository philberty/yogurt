#!/usr/bin/env python3

import os
import Yogurt

from distutils.core import setup, Command

setup (
    name = "Yogurt",
    version = Yogurt.__version__,
    url = Yogurt.__url__,
    author = Yogurt.__author__,
    author_email = Yogurt.__email__,
    license = "MIT",
    description = 'A feed Aggregator Starcraft',
    platforms = ('Any',),
    keywords = ('web', 'sc2', 'feeds'),
    packages = ['Yogurt'],
    scripts = ['bin/yogurt.py', 'bin/feeder.py'],
    package_data = {'Yogurt': ['www']},
    data_files = [('/etc/yogurt/', ['etc/yogurt/yogurt.cfg'])]
)
