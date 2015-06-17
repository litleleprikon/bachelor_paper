#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tweepy.streaming import StreamListener
from datetime import datetime, timedelta
import json

__author__ = 'litleleprikon'


class Listener(StreamListener):
    def __init__(self, f: 'open()', places):
        self._places = places
        self._file = f
        self._end_time = datetime.now() + timedelta(hours=3)

    def on_data(self, raw_data):
        if datetime.now() > self._end_time:
            return False
        self._print_tweet(raw_data)
        return True

    def _get_place(self, location: list):
        lng, lat = location
        result = 'undefined'
        for place in self._places:
            if place['southwest']['lat'] <= lat <= place['northeast']['lat'] \
                    and place['southwest']['lng'] <= lng <= place['northeast']['lng']:
                result = place['name']
                break
        return result

    def _print_tweet(self, tweet):
        tweet = json.loads(tweet)
        if tweet['coordinates'] is not None:
            self._file.write('{0}\t{1}\n'.format(*self._process_tweet(tweet)))

    def _process_tweet(self, tweet):
        text = tweet['text']
        place = self._get_place([i for i in map(float, tweet['coordinates']['coordinates'])])
        return place, text.replace('\n', ' ').replace('\t', ' ')

    def on_error(self, status_code):
        print('code: {0}'.format(status_code))
