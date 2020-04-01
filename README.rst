################
Prime Factorizer
################

:Author: Aaron Dallas

Find the prime factors for a positive integer

Synopsis
========

::
 factor_primes.py --no-cache --cache-file="my-cache-file.dbm" [int]

Description
===========

This module finds the prime factors for a given integer and caches
its results in a dbm file. The cache file may be specified; if not
a default cache file will be created and persist.
