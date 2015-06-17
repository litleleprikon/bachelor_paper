#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import stdin
from decimal import Decimal, getcontext


__author__ = 'litleleprikon'


def main():
    getcontext().prec = 6
    last_key, count, last_sum = None, 0, Decimal(0.0)
    for line in stdin:
        key, value = line.split('\t', maxsplit=1)

        if last_key is not None and last_key != key:
            result = last_sum/count
            print('{}\t{}'.format(last_key, result))
            count, last_sum = 0, Decimal(0.0)

        last_key = key
        last_sum += Decimal(value)
        count += 1

    print('{}\t{}'.format(last_key, last_sum/count))



if __name__ == '__main__':
    main()
