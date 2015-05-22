#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app_libs.config_reader import ConfigReader
from app_libs.main_runner import MainRunner


__author__ = 'litleleprikon'


def main():
    try:
        with open('config.json', 'r') as f:
            config = ConfigReader(f)
            pass
    except FileNotFoundError:
        print('No config File\n')
        exit()
    if config.error:
        print(config.error)
        exit()
    MainRunner(config)


if __name__ == '__main__':
    main()