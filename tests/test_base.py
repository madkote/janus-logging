#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests.test_base
'''
:author:    madkote
:contact:   madkote(at)bluewin.ch
:copyright: Copyright 2019, madkote

tests.test_base
---------------
Package
'''

from __future__ import absolute_import

import asyncio
import logging
import sys
import unittest

import janus_logging

VERSION = (1, 0, 0)

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)
__copyright__ = 'Copyright 2019, madkote'


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_duplicate(self):
        counter = 4
        name = 'test_unit_janus_logger'
        level = logging.DEBUG
        stream = sys.stdout
        loop = asyncio.get_event_loop()

        logger = janus_logging.JanusLogger(
            name=name,
            level=level,
            loop=loop,
            fixture=janus_logging.fixture_json,
            stream=stream,
            extra=dict(bla='blabla')
        )
        print(logger.logger_sync(logger_name='test_logger_sync').logger.handlers)
        logger = janus_logging.JanusLogger(
            name=name,
            level=level,
            loop=loop,
            fixture=janus_logging.fixture_json,
            stream=stream,
            extra=dict(bla='blabla')
        )
        print(logger.logger_sync(logger_name='test_logger_sync').logger.handlers)
        logger.shutdown()
        #
        #
        loop.close()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
