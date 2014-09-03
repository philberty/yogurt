import shelve

class Cache:
    def __init__(self, config):
        self._shelve = shelve.open(config['file'], flag=config['flags'])

    def get(self, key):
        return self._shelve[key]

    def set(self, key, value):
        self._shelve[key] = value
