#!/usr/bin/env python3

from argparse import ArgumentParser
from integer_factorizer import IntegerFactorizer


def parse_args():
    argp = ArgumentParser("Factor the primes of an integer")

    argp.add_argument("n", metavar="N", type=int, help="integer to find prime factors for")
    argp.add_argument("--no-cache", dest="no_cache", action="store_true", help="do not use the internal cache")
    argp.add_argument("--cache-file", dest="cache_file", default=None, help="a custom cache file to use. NOTE: the file must have a valid dbm extension")

    return argp.parse_args()


def main():
    args = parse_args()

    print(args.n, ": ", end="")

    if args.no_cache:
        print(" ".join((str(x) for x in IntegerFactorizer.gen_prime_factors(args.n))))
    else:
        ifact = IntegerFactorizer(cache_file=args.cache_file)
        print(" ".join((str(x) for x in ifact.prime_factors(args.n))))

    return 0


if __name__ == "__main__":
    quit(main())
