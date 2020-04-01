import math
import shelve
from typing import Iterator, List


class IntegerFactorizer:
    """
    Factor integers
    Cache results
    """
    def __init__(self, cache_file=None):
        if cache_file is None:
            cache_file = ".integer_factorizer_cache.dbm"

        self.__cache_file = cache_file
        self.__cache = shelve.open(cache_file)

    def __del__(self):
        self.__cache.close()

    @staticmethod
    def gen_prime_factors(n: int) -> Iterator[int]:
        """
        Iterate over the prime factors for a given integer
        Will return empty for integers <= 1

        :param n: integer to factor
        :return: prime factors
        :rtype: Iterator[int]
        """
        if n <= 1:
            return

        # Get 2's dividing n
        while n % 2 == 0:
            yield 2
            n //= 2

        # Current n is odd, step by 1
        n_sqrt_floor = math.floor(math.sqrt(n))
        for i in range(3, n_sqrt_floor + 1, 2):
            while n % i == 0:
                yield i
                n //= i

        # If current n is still > 0, it must itself by prime
        if n > 2:
            yield n

    def prime_factors(self, n: int) -> List[int]:
        """
        Get a list of prime factors for a given integer
        Will return results from an internal cache, if available

        :param n: integer to factor
        :return: prime factors
        :rtype: List[int]
        """
        n_str = str(n)  # shelve requires that keys be strings
        if n_str not in self.__cache:
            self.__cache[n_str] = list(self.gen_prime_factors(n))
            self.__cache.sync()

        return self.__cache[n_str]
