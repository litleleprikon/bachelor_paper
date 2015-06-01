#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import stdin


__author__ = 'litleleprikon'


def main():
    last_key, count = None, 0
    for line in stdin:
        key, value = line.split('\t', maxsplit=1)

        if last_key is not None and last_key != key:
            print('{}\t{}'.format(last_key, count))
            count = 0

        last_key = key
        count += int(value)

    print('{}\t{}'.format(last_key, count))



if __name__ == '__main__':
    main()
