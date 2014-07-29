import shelve

class Cache:
    def __init__ (self, config):
        self.__cache = { }

    def get (self, key):
        try:
            return self.__cache [key]
        except:
            return None

    def set (self, key, value):
        self.__cache [key] = value
