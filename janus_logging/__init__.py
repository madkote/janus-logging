#!/usr/bin/env python
# -*- coding: utf-8 -*-
# janus_logging.__init__
'''
:author:    mdakote
:contact:   madkote(at)bluewin.ch
:copyright: Copyright 2019, madkote

janus_logging
-------------
Janus logging
'''

from __future__ import absolute_import

import asyncio
import datetime
import json
import logging
import sys
import typing

from aiologger import Logger as aioLogger
from aiologger.formatters.json import ExtendedJsonFormatter
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.loggers.json import JsonLogger as aioJsonLogger
from aiologger.records import LogRecord as aioLogRecord

from .version import VERSION

__all__ = [
    'JanusLogger',
    'AsyncLoggerAdapter', 'SyncLoggerAdapter', 'AsyncNullHandler',
    'fixture_sync_default', 'fixture_sync_json',
    'fixture_async_default', 'fixture_async_json',
]
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)
__copyright__ = 'Copyright 2019, madkote'


class ILoggerAdapter(object):
    '''
    Logger adapter interface
    '''
    def process(self, msg: str, kwargs: typing.Dict) -> (str, typing.Dict):
        '''
        Process message and keyword arguments - update `extra` from adapter
        :param msg:
        :param kwargs:
        :return: tuple with message and keyword arguments
        '''
        if 'extra' not in kwargs:
            kwargs['extra'] = self.extra
        elif isinstance(kwargs['extra'], dict):
            kwargs['extra'] = {**self.extra, **kwargs['extra']}
        else:
            kwargs['extra'] = self.extra
        return msg, kwargs


class AsyncNullHandler(logging.NullHandler):
    '''
    Async NULL handler - ignore any log record.
    '''
    async def close(self) -> None:
        pass

    def createLock(self) -> None:
        self.lock = None

    async def emit(self, record: aioLogRecord) -> None:
        pass

    async def flush(self) -> None:
        pass

    async def handle(self, record: aioLogRecord) -> bool:  # @UnusedVariable
        return True

    async def handle_error(self, record: aioLogRecord, exception: Exception) -> None:  # @IgnorePep8
        pass


class AsyncLoggerAdapter(ILoggerAdapter):
    '''
    Async logger adapter
    '''
    def __init__(self, logger: aioLogger, extra: typing.Dict):
        '''
        Constructor with logger and extra fields
        :param logger: logger to be wrapped
        :param extra: extra arguments for log record
        '''
        self.logger = logger
        self.extra = extra

    def debug(self, msg, *args, **kwargs) -> asyncio.Task:
        return self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs) -> asyncio.Task:
        return self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs) -> asyncio.Task:
        return self.log(logging.WARNING, msg, *args, **kwargs)

    warn = warning

    def error(self, msg, *args, **kwargs) -> asyncio.Task:
        return self.log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs) -> asyncio.Task:
        return self.log(logging.ERROR, msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs) -> asyncio.Task:
        return self.log(logging.CRITICAL, msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs) -> asyncio.Task:
        msg, kwargs = self.process(msg, kwargs)
        return self.logger._make_log_task(level, msg, args, **kwargs)

    async def shutdown(self) -> None:
        await self.logger.shutdown()

    @property
    def name(self):
        return self.logger.name


class SyncLoggerAdapter(logging.LoggerAdapter, ILoggerAdapter):
    '''
    Sync logger adapter
    '''
    def process(self, msg: str, kwargs: typing.Dict):
        return ILoggerAdapter.process(self, msg, kwargs)


class SyncJsonFormatter(logging.Formatter):
    '''
    Sync Json logging formatter
    '''
    RESERVED_ATTRS = (
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'levelname', 'levelno', 'lineno', 'module',
        'msecs', 'message', 'msg', 'name', 'pathname', 'process',
        'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName'
    )

    def __init__(self, serializer: typing.Callable[..., str]=None, **kwargs):
        '''
        Constructor with serializer to be used and keyword arguments
        :param serializer: function for serialization
        '''
        if serializer is None:
            serializer = json.dumps
        super(SyncJsonFormatter, self).__init__()
        self.extra = kwargs
        self.serializer = serializer

    def get_record_extra(
            self,
            record: logging.LogRecord,
            reserved: typing.Set
            ) -> typing.Dict:
        '''
        Get the dictionary with extra fields of the log record
        :param record: log record
        :param reserved: set  with reserved attributes of a log record
        :return: dictionary with extra fields of the log record
        '''
        return dict(
            (key, value)
            for key, value in record.__dict__.items()
            if (
                key not in reserved and
                not (hasattr(key, 'startswith') and
                     key.startswith('_'))
            )
        )

    def format(self, record: logging.LogRecord) -> str:
        '''
        Format log record
        :param record: log record
        :return: log string
        '''
        details = {
            **self.extra,
            **self.get_record_extra(record, self.RESERVED_ATTRS)
        }
        details.update(
            logged_at=datetime.datetime.now(datetime.timezone.utc).astimezone(None).isoformat(),  # @IgnorePep8
            line_numer=record.lineno,
            function=record.funcName,
            level=record.levelname.upper(),
            msg=record.msg,
            file_path=record.pathname
        )
        return self.serializer(details)


def fixture_sync_default(name: str, level: int, **kwargs) -> logging.Logger:
    '''
    Default sync logger constructor
    :param name: logger name
    :param level: logging level
    :return: logger
    '''
    stream = kwargs.pop('stream', sys.stdout)
    #
    logger = logging.getLogger(name=name)
    logger.setLevel(level)
    hdlr = logging.StreamHandler(stream=stream)
    hdlr.setLevel(level)
    logger.addHandler(hdlr)
    return logger


def fixture_sync_json(name: str, level: int, **kwargs) -> logging.Logger:
    '''
    Json sync logger constructor
    :param name: logger name
    :param level: logging level
    :return: logger with Json format
    '''
    extra = kwargs.pop('extra', {})
    serializer = kwargs.pop('serializer', json.dumps)
    stream = kwargs.pop('stream', sys.stdout)
    #
    logger = logging.getLogger(name=name)
    logger.setLevel(level)
    fmt = SyncJsonFormatter(serializer=serializer, **extra)
    hdlr = logging.StreamHandler(stream=stream)
    hdlr.setLevel(level)
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    return logger


def fixture_async_default(
        name: str,
        level: int,
        loop: asyncio.AbstractEventLoop,
        **kwargs
        ) -> aioLogger:
    '''
    Default async logger constructor
    :param name: logger name
    :param level: logging level
    :param loop: event loop
    :return: sync logger
    '''
    stream = kwargs.pop('stream', sys.stdout)
    #
    logger = aioLogger(name=name, level=level, loop=loop)
    logger.add_handler(
            AsyncStreamHandler(
                stream=stream,
                level=level,
                formatter=None,
                filter=None,
                loop=loop,
            )
        )
    return logger


def fixture_async_json(
        name: str,
        level: int,
        loop: asyncio.AbstractEventLoop,
        **kwargs
        ) -> aioLogger:
    '''
    Json async logger constructor
    :param name: logger name
    :param level: logging level
    :param loop: event loop
    :return: logger with Json format
    '''
    extra = kwargs.pop('extra', {})
    stream = kwargs.pop('stream', sys.stdout)
    serializer = kwargs.pop('serializer', json.dumps)
    #
    logger = aioJsonLogger(name=name, level=level, extra=extra, loop=loop)
    formatter = ExtendedJsonFormatter(serializer=serializer)
    logger.add_handler(
            AsyncStreamHandler(
                stream=stream,
                level=level,
                formatter=formatter,
                filter=None,
                loop=loop,
            )
        )
    return logger


class JanusLogger(object):
    '''
    Janus logger
    '''
    def __init__(
            self,
            name: str=__name__,
            level: int=logging.WARNING,
            loop: asyncio.AbstractEventLoop=None,
            fixture_async: typing.Callable[..., aioLogger]=None,
            fixture_sync: typing.Callable[..., logging.Logger]=None,
            **kwargs
            ) -> None:
        '''
        Constructor
        :param name: name of the logger
        :param level: logging level
        :param loop: event loop
        :param fixture_async: logging fixture for async logger
        :param fixture_sync: logging fixture for sync logger
        '''
        if loop is None:
            loop = asyncio.get_event_loop()
        if fixture_async is None:
            fixture_async = fixture_async_default
        if fixture_sync is None:
            fixture_sync = fixture_sync_default

        self.name = name

        self._extra = kwargs.pop('extra', {})
        self._level = level
        self._loop = loop
        self._log_sync = fixture_sync(name, level, **kwargs)
        self._log_async = fixture_async(name, level, loop, **kwargs)

    def shutdown(self) -> None:
        '''
        Shutdown logging
        '''
        self._loop.run_until_complete(
            asyncio.gather(
                self._log_async.shutdown(),
                self._loop.run_in_executor(
                    None,
                    logging.shutdown,
                )
            )
        )

    def logger_async(self, **kwargs) -> AsyncLoggerAdapter:
        '''
        Get async logger
        :return: async logger
        '''
        return AsyncLoggerAdapter(self._log_async, {**self._extra, **kwargs})

    def logger_sync(self, **kwargs) -> SyncLoggerAdapter:
        '''
        Get sync logger
        :return: sync logger
        '''
        return SyncLoggerAdapter(self._log_sync, {**self._extra, **kwargs})
