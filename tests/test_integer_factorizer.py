import math
import pytest
from tempfile import NamedTemporaryFile
from hypothesis import given, settings
from hypothesis.strategies import integers
from integer_factorizer import IntegerFactorizer


@pytest.fixture(scope="session")
def intfact():
    cache_file = NamedTemporaryFile()

    # Persist this object throughout the lifecycle of the test
    yield IntegerFactorizer(cache_file=cache_file.name + ".dbm")

    return


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True

    # Quick check to see if the number is even
    if n > 2 and n % 2 == 0:
        return False

    # Step through all odd numbers up to the floor of the square root
    n_sqrt_floor = math.floor(math.sqrt(n))
    for i in range(3,  n_sqrt_floor + 1, 2):
        if i % 2 == 0:
            return False

    # The number is prime
    return True


@settings(max_examples=100)
@given(s=integers(max_value=9_000_000))
def test_gen_integer_factors(s):
    f = list(IntegerFactorizer.gen_prime_factors(s))

    if len(f) > 0:
        product = 1
        for x in f:
            product *= x
            assert is_prime(x), "factor {0} is not prime".format(x)

        assert product == s, "factors do not produce n"
    else:
        assert s <= 1, "no factors found"


@settings(max_examples=10)
@given(s=integers(max_value=9_000_000))
def test_integer_factors(intfact, s):
    f = list(intfact.prime_factors(s))

    if len(f) > 0:
        product = 1
        for x in f:
            product *= x
            assert is_prime(x), "factor {0} is not prime".format(x)

        assert product == s, "factors do not produce n"
    else:
        assert s <= 1, "no factors found"
