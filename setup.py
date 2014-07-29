from distutils.core import setup

setup (
    name = "Yogurt",
    version = "0.1",
    url = 'https://github.com/redbrain/yogurt',
    author = 'Philip Herron',
    author_email = 'redbrain@gcc.gnu.org',
    license = "MIT",
    description = 'A feed Aggregator Starcraft',
    platforms = ('Any',),
    keywords = ('web', 'sc2', 'feeds'),
    packages = ['Yogurt'],
    scripts = ['yogurt.py'],
    package_data = {'Yogurt': ['www']},
    data_files=[('/etc/yogurt/', ['etc/yogurt/yogurt.cfg'])],
)
