#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import stdin, stderr
import re
from pymongo import MongoClient
__author__ = 'litleleprikon'

REGEX = re.compile(r'((\b[^\s]+\b)((?<=\.\w).)?)')

# Texas, USA	I'm bot rude I'm outspoken


def main():
    client = MongoClient()
    # dictionary = client.sentiment.dictionary
    for line in stdin:
        try:
            key, value = line.split('\t', maxsplit=1)
            value = len(value)
            # value = ' '.join(map(stem, REGEX.findall(value)))
            print('{0}\t{1}'.format(key, value))
        except Exception as ex:
            stderr.write(line)


if __name__ == '__main__':
    main()
