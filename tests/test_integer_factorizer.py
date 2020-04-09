import math
import pytest
from re import match
from tempfile import NamedTemporaryFile
from hypothesis import given, settings
from hypothesis.strategies import integers
from integer_factorizer import IntegerFactorizer, AbstractCacher, __version__
from integer_factorizer.shelve_cacher import ShelveCacher


@pytest.fixture(scope="module")
def fake_cached_int_fact():
    """
    Fixture for a fake cacher that does no caching
    but has the correct methods
    """
    class FakeCache(AbstractCacher):
        def save(self, key, value):
            pass

        def get(self, key):
            pass

    yield IntegerFactorizer(cacher=FakeCache())

    return


@pytest.fixture(scope="module")
def cached_int_fact():
    """
    Fixture that uses the contained ShelveCacher
    """
    cache_file = NamedTemporaryFile()
    cacher = ShelveCacher(cache_file=cache_file.name + ".dbm")

    # Persist this object throughout the lifecycle of the test
    yield IntegerFactorizer(cacher=cacher)

    return


@pytest.fixture(scope="module")
def int_fact():
    """
    Fixture with no cache
    """
    yield IntegerFactorizer()

    return


def is_prime(n: int) -> bool:
    """Internal test method to determine if a number is prime"""
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
    """Test the static method to generate prime factors"""
    f = list(IntegerFactorizer.gen_prime_factors(s))

    if len(f) > 0:
        product = 1
        for x in f:
            product *= x
            assert is_prime(x), "factor {0} is not prime".format(x)

        assert product == s, "factors do not produce n"
    else:
        assert s <= 1, "no factors found"


@settings(max_examples=100)
@given(s=integers(max_value=9_000_000))
def test_integer_factors_with_cache(cached_int_fact, s):
    """Test with the given ShelveCacher using a named temp file for a DBM"""
    f = list(cached_int_fact.prime_factors(s))

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
def test_integer_factors_nocache(int_fact, s):
    """Test with no cacher"""
    f = list(int_fact.prime_factors(s))

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
def test_integer_factors_fake_cache(fake_cached_int_fact, s):
    """Test using a mock cacher that does nothing"""
    f = list(fake_cached_int_fact.prime_factors(s))

    if len(f) > 0:
        product = 1
        for x in f:
            product *= x
            assert is_prime(x), "factor {0} is not prime".format(x)

        assert product == s, "factors do not produce n"
    else:
        assert s <= 1, "no factors found"


def test_version():
    """Confirm that the version is exported correctly"""
    assert match(r'^\d+\.\d+\.\d+$', __version__)


def test_bad_cacher():
    """Test attempting to use an invalid object as a cacher"""
    with pytest.raises(ValueError) as e:
        ifact = IntegerFactorizer(cacher=str)
        _ = list(ifact.prime_factors(1000))

    assert "subclass AbstractCacher" in str(e)
