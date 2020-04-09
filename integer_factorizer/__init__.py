import math
from abc import ABC, abstractmethod
from typing import Iterator, List, Type, Hashable, Any
from ._version import __version__


class AbstractCacher(ABC):
    """
    Abstract Class to implement a cacher

    I like abstract classes especially when combined with a Factory,
    but in this instance duck type testing could also work, i.e.:

    if not hasattr(cacher, 'save') or not hasattr(cacher, 'get'):
        raise ValueError
    """
    @abstractmethod
    def save(self, key: Hashable, value: Any):
        pass

    @abstractmethod
    def get(self, key: Hashable):
        pass


class IntegerFactorizer:
    """
    Factor integers
    Cache results
    """
    def __init__(self, cacher: Type[AbstractCacher]=None):
        if cacher is not None:
            if not issubclass(cacher.__class__, AbstractCacher):
                raise ValueError("value of cacher must subclass AbstractCacher")
            self.__cacher = cacher
        else:
            self.__cacher = None

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
        val = None
        if self.__cacher is not None:
            val = self.__cacher.get(n)
            if val is None:
                val = list(self.gen_prime_factors(n))
                self.__cacher.save(n, val)
        else:
            val = list(self.gen_prime_factors(n))

        return val
