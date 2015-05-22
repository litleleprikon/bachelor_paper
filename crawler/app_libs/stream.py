#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tweepy.streaming import StreamListener
from datetime import datetime, timedelta
import json

__author__ = 'litleleprikon'


class Listener(StreamListener):
    def __init__(self, f: 'open()'):
        self._file = f
        self._end_time = datetime.now() + timedelta(hours=1)

    def on_data(self, raw_data):
        if datetime.now() > self._end_time:
            return False
        self._print_tweet(raw_data)
        return True

    def _print_tweet(self, tweet):
        self._file.write('{0}\t{1}\n'.format(*self._process_tweet(tweet)))

    def _process_tweet(self, tweet):
        tweet = json.loads(tweet)
        text = tweet['text']
        location = tweet['place']['full_name']
        return location, text.replace('\n', ' ').replace('\t', ' ')

    def on_error(self, status_code):
        print('code: {0}'.format(status_code))
