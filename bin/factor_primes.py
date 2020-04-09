#!/usr/bin/env python3

from argparse import ArgumentParser
from integer_factorizer import IntegerFactorizer
from integer_factorizer.shelve_cacher import ShelveCacher


def parse_args():
    argp = ArgumentParser("Factor the primes of an integer")

    argp.add_argument("n", metavar="N", type=int, help="integer to find prime factors for")
    argp.add_argument("--cache-file", dest="cache_file", default=None,
                      help="Use this DBM file to cache results between runs. Must end in extension .dbm")

    return argp.parse_args()


def main():
    args = parse_args()

    print(args.n, ": ", end="")

    cacher = None
    if args.cache_file is not None:
        if not args.cache_file.endswith('.dbm'):
            raise UserWarning("given cache file must have .dbm extension")
        cacher = ShelveCacher(cache_file=args.cache_file)

    ifact = IntegerFactorizer(cacher=cacher)
    print(" ".join((str(x) for x in ifact.prime_factors(args.n))))

    return 0


if __name__ == "__main__":
    quit(main())
