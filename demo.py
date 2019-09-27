#!/usr/bin/env python
# -*- coding: utf-8 -*-
# demo
'''
:author:    mdakote
:contact:   madkote(at)bluewin.ch
:copyright: Copyright 2019, madkote

demo
----
Demo the functionality
'''

from __future__ import absolute_import

import asyncio
import logging
import sys

import aiologger
import janus_logging

VERSION = (1, 0, 0)

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)
__copyright__ = 'Copyright 2019, madkote'


def threaded(sync_log, counter: int):
    for i in range(counter):
        sync_log.info(
            's-Hello #%s' % i,
            extra=dict(counter=i, log_type='sync', log_status='in progress')
        )
    sync_log.info(
        's-Finished #%s' % counter,
        extra=dict(total=counter, log_type='sync', log_status='finished')
    )


async def async_coro(async_log, counter: int):
    for i in range(counter):
        await async_log.info(
            'aio-Hello #%s' % i,
            extra=dict(counter=i, log_type='async', log_status='in progress')
        )
    await async_log.info(
        'aio-Finished #%s' % counter,
        extra=dict(total=counter, log_type='async', log_status='finished')
    )


def custom_fixture_sync(name: str, level: int, **kwargs) -> logging.Logger:
    ...
    return ...


def fixture_async_default(
        name: str,
        level: int,
        loop: asyncio.AbstractEventLoop,
        **kwargs
        ) -> aiologger.Logger:
    ...
    return ...


def main():
    counter = 4
    name = 'my_janus_logger'
    level = logging.DEBUG
    stream = sys.stdout
    loop = asyncio.get_event_loop()
    #
    logger = janus_logging.JanusLogger(
        name=name,
        level=level,
        loop=loop,
        fixture_async=janus_logging.fixture_async_json,
        fixture_sync=janus_logging.fixture_sync_json,
        stream=stream,
        extra=dict(bla='blabla')
    )
    loop.run_until_complete(
        asyncio.gather(
            loop.run_in_executor(
                None,
                threaded,
                logger.logger_sync(logger_name='logger_sync'),
                counter
            ),
            async_coro(
                logger.logger_async(logger_name='logger_async'),
                counter
            )
        )
    )
    logger.shutdown()
    #
    #
    loop.close()


if __name__ == '__main__':
    main()
