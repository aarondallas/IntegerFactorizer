import shelve
from . import AbstractCacher


class ShelveCacher(AbstractCacher):
    """
    Implementation of the abstract cacher using the Shelve library and DBM files
    """
    def __init__(self, cache_file=None):
        if cache_file is None:
            cache_file = ".integer_factorizer_cache.dbm"

        self.__cache_file = cache_file
        self.__cache = shelve.open(cache_file)

    def __del__(self):
        self.__cache.close()

    def save(self, key, value):
        # Shelve keys must be strings
        if not isinstance(key, str):
            key = str(key)

        self.__cache[key] = value

    def get(self, key):
        # Returns None if key not in cache
        # Shelve keys must be strings
        if not isinstance(key, str):
            key = str(key)

        return self.__cache.get(key)
