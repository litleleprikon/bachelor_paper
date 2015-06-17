#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tweepy import OAuthHandler, Stream
from app_libs.stream import Listener
from os import path
__author__ = 'litleleprikon'


class MainRunner:
    def __init__(self, conf):
        self._conf = conf
        self._out = None
        self.listeners = []
        self._auth = OAuthHandler(conf.consumer_key, conf.consumer_secret)
        self._auth.set_access_token(conf.access_token, conf.access_token_secret)
        self._run_listener()

    def _run_listener(self):
        listener = Listener(self.out, self._conf.places)
        stream = Stream(self._auth, listener)
        locations = []
        for city in self._conf.places:
            locations.extend(city['southwest'].values())
            locations.extend(city['northeast'].values())
        stream.filter(locations=locations)

    @property
    def out(self):
        if self._out is None:
            try:
                self._out = open(self._conf.output, 'a')
            except FileNotFoundError:
                if path.exists('output.txt'):
                    self._out = open('output.txt', 'a')
                else:
                    self._out = open('output.txt', 'a')
        return self._out

    def __del__(self):
        self.out.close()
