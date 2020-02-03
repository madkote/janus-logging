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
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_00_duplicate_sync(self):
        name = 'test_unit_janus_logger'
        level = logging.DEBUG
        stream = sys.stdout
        num_handlers_exp = 1
        try:
            loop = self.loop
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            #
            #
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            #
            #
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            #
            #
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
        finally:
            logger.shutdown()

    def test_01_duplicate_sync(self):
        name = 'test_unit_janus_logger'
        level = logging.DEBUG
        stream = sys.stdout
        num_handlers_exp = 1
        try:
            loop = self.loop
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            #
            #
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            #
            #
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            #
            #
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
        finally:
            logger.shutdown()
        #
        #
        try:
            loop = self.loop
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            #
            #
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            #
            #
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            #
            #
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_sync(
                    logger_name='test_logger_sync'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
        finally:
            logger.shutdown()

    def test_10_duplicate_async(self):
        name = 'test_unit_janus_logger'
        level = logging.DEBUG
        stream = sys.stdout
        num_handlers_exp = 1
        try:
            loop = self.loop
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
        finally:
            logger.shutdown()

    def test_11_duplicate_async(self):
        name = 'test_unit_janus_logger'
        level = logging.DEBUG
        stream = sys.stdout
        num_handlers_exp = 1
        try:
            loop = self.loop
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
        finally:
            logger.shutdown()
        #
        #
        try:
            loop = self.loop
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#1b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            logger = janus_logging.JanusLogger(
                name=name,
                level=level,
                loop=loop,
                fixture=janus_logging.fixture_json,
                stream=stream,
                extra=dict(bla='blabla')
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2a More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
            num_handlers_res = len(
                logger.logger_async(
                    logger_name='test_logger_async'
                ).logger.handlers
            )
            self.assertTrue(
                num_handlers_exp == num_handlers_res,
                '#2b More handler as expected [exp]=%s != [res]=%s' % (
                    num_handlers_exp, num_handlers_res
                )
            )
        finally:
            logger.shutdown()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
