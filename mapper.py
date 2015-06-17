#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import stdin, stderr
import re
import numpy as np
from pymongo import MongoClient
__author__ = 'litleleprikon'


HASHTAG_RE = re.compile(r'#[-a-z0-9+&@#/%?=~_()|!:,.;]+', re.IGNORECASE)
FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')
PROFILE_RE = re.compile(r'@[-a-z0-9+&@#/%?=~_()|!:,.;]+', re.IGNORECASE)
LINK_RE = re.compile(r'(\(.*?)?\b((?:https?)://[-a-z0-9+&@#/%?=~_()|!:,.;]*[-a-z0-9+&@#/%=~_()|])',
                     re.IGNORECASE)
SPLIT_RE = re.compile(r" |(?<! |[',\\.:!()@/<>])(?=[',\\.:!()@/<>])|(?<=[',\\.:!()@/<>])(?![',\\.:!()@/<>])",
                      re.IGNORECASE)

# Texas, USA	I'm bot rude I'm outspoken
# Example	Sundar Pichai: Why @Google can afford to be patient http://for.tn/1HRW3Wb
# Example	That’s a wrap. Catch up with everything you missed during today’s keynote: http://g.co/go/io2015blog  #io15
# Example	a spot-on addition: http://pamelaclark.tumblr.com/post/89366678584/36 … RT @gvanrossum: "When a woman tells you something is sexist, believe her." http://pamelaclark.tumblr.com/post/871137111
# Example	Play for Families will make it easier for #sdf parents to find games, books, movies & more for their kids. http://goo.gl/dYSakn  #io15


def convert(tags):
    for tag in tags:
        s1 = FIRST_CAP_RE.sub(r'\1 \2', tag[1:])
        yield ALL_CAP_RE.sub(r'\1 \2', s1).lower()



def main():
    client = MongoClient()
    dictionary = client.sentiment.dictionary
    for line in stdin:
        try:
            key, value = line.split('\t', maxsplit=1)
            hashtags = HASHTAG_RE.findall(value)
            if len(hashtags):
                hashtags = convert(hashtags)

            for tag in hashtags:
                value = HASHTAG_RE.sub(tag, value, count=1)

            value = PROFILE_RE.sub('', value)
            value = LINK_RE.sub('', value)
            value = map(str.lower, SPLIT_RE.split(value))

            words = [i for i in value if i != '' and i != ' ']
            words_list = dictionary.find({'word': {'$in': words}})
            happy_vaues, sad_values = [], []
            for word in words_list:
                happy_values.append(word['happy'])
                sad_values.append(word['sad'])

            happy_log_value = np.sum(happy_values)
            sad_log_value = np.sum(sad_values)

            prob_happy = np.reciprocal(np.exp(sad_log_value - happy_log_value) + 1)
            result = np.round(prob_happy)

            print('{0}\t{1}'.format(key, result))

        except Exception as ex:
            stderr.write('\n[ERROR]\n{}\n{}[/ERROR]\n'.format(ex, line))


if __name__ == '__main__':
    main()
