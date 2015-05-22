#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


__author__ = 'litleleprikon'


class ConfigReader:
    FIELDS = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret', 'places', 'output')

    def __init__(self, settings_file):
        self._errors = ''
        try:
            self._data = json.load(settings_file)
        except ValueError:
            self._errors += 'File is not valid\n'
            return
        for name in self.FIELDS:
            self._check_field(name)

    def _check_field(self, name):
        value = self._data.get(name)
        if value is None:
            self._errors += 'Value "{0:s}" not found\n'.format(name)
            return
        setattr(self, name, value)

    @property
    def error(self):
        if self._errors:
            return ''.join(['ConfigReader error: {0:s}\n'.format(error) for error in self._errors.split('\n')])
        return False