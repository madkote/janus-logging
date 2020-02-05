#!/usr/bin/env python
# -*- coding: utf-8 -*-
# janus_logging.__init__
'''
:author:    madkote
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
import os
import sys
import typing

from aiologger import Logger as aioLogger
# from aiologger.formatters.json import ExtendedJsonFormatter
from aiologger.handlers.streams import AsyncStreamHandler as _AsyncStreamHandler  # noqa E501
# from aiologger.loggers.json import JsonLogger as aioJsonLogger
from aiologger.records import LogRecord as aioLogRecord

from .version import VERSION

__all__ = [
    'JanusLogger',
    'AsyncLoggerAdapter', 'SyncLoggerAdapter',
    'AsyncNullHandler', 'AsyncStreamHandler',
    'fixture_default', 'fixture_json', 'has_logger_by_name',
]
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)
__copyright__ = 'Copyright 2019, madkote'


class AsyncStreamHandler(_AsyncStreamHandler):
    def __init__(self, *args, **kwargs):
        super(AsyncStreamHandler, self).__init__(*args, **kwargs)
        self._stream = None

    async def _init_writer(self) -> asyncio.StreamWriter:
        async with self._initialization_lock:
            if self.writer is not None:
                return self.writer
            self._stream = os.fdopen(os.dup(self.stream.fileno()), 'wb')
            transport, protocol = await self.loop.connect_write_pipe(
                self.protocol_class, self._stream
            )
            self.writer = asyncio.StreamWriter(
                transport=transport,
                protocol=protocol,
                reader=None,
                loop=self.loop,
            )
            return self.writer

    async def close(self):
        try:
            if self.writer is None:
                return
            await self.flush()
            self.writer.close()
        finally:
            if self._stream is not None:
                self._stream.close()


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

    async def handle_error(self, record: aioLogRecord, exception: Exception) -> None:  # noqa E501
        pass


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


class AsyncLoggerAdapter(ILoggerAdapter):
    '''
    Async logger adapter
    '''
    def __init__(
            self,
            logger: aioLogger,
            extra: typing.Dict,
            loop: asyncio.AbstractEventLoop
    ):
        '''
        Constructor with logger, extra fields and loop
        :param logger: logger to be wrapped
        :param extra: extra arguments for log record
        :param loop: event loop
        '''
        self.logger = logger
        self.extra = extra
        self.loop = loop
        self._dummy_task: typing.Optional[asyncio.Task] = None

    def __make_dummy_task(self) -> asyncio.Task:
        async def _dummy(*args, **kwargs):  # @UnusedVariable
            return
        return self.loop.create_task(_dummy())

    def log(self, level, msg, *args, **kwargs) -> asyncio.Task:
        def _task(_func_or_method, _level, _msg, _args, _kwargs):
            _func_or_method(_level, _msg, *_args, **_kwargs)

        if not self.isEnabledFor(level):
            if self._dummy_task is None:
                self._dummy_task = self.__make_dummy_task()
            return self._dummy_task

        msg, kwargs = self.process(msg, kwargs)

        async def _coro():
            return await self.loop.run_in_executor(
                None,
                _task,
                self.logger.log,
                level,
                msg,
                args,
                kwargs
            )

        return self.loop.create_task(_coro())

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

    fatal = critical

    def isEnabledFor(self, level):
        return self.logger.isEnabledFor(level)

    def setLevel(self, level):
        self.logger.setLevel(level)

    def getEffectiveLevel(self):
        return self.logger.getEffectiveLevel()

    def hasHandlers(self):
        return self.logger.hasHandlers()

    @property
    def manager(self):
        return self.logger.manager

    @manager.setter
    def manager(self, value):
        self.logger.manager = value

    @property
    def name(self):
        return self.logger.name

    def __repr__(self):
        logger = self.logger
        level = logging.getLevelName(logger.getEffectiveLevel())
        return '<%s %s (%s)>' % (self.__class__.__name__, logger.name, level)


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
                key not in reserved and not (
                    hasattr(key, 'startswith') and key.startswith('_')
                )
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
            logged_at=datetime.datetime.now(datetime.timezone.utc).astimezone(None).isoformat(),  # noqa E501
            line_numer=record.lineno,
            function=record.funcName,
            level=record.levelname.upper(),
            msg=record.getMessage(),
            file_path=record.pathname
        )
        return self.serializer(details)


def has_logger_by_name(name: str) -> bool:
    '''
    Check if a logger with given name already available.
    :param name: Name of the logger
    :return: `True` if a logger with given name already available,
        otherwise `False`.
    '''
    return name in logging.Logger.manager.loggerDict  # @UndefinedVariable


def fixture_default(
        name: str,
        level: int,
        loop: asyncio.AbstractEventLoop,  # @UnusedVariable
        **kwargs
) -> logging.Logger:
    '''
    Default logger constructor
    :param name: logger name
    :param level: logging level
    :param loop: event loop
    :return: logger
    '''
    if has_logger_by_name(name):
        return logging.getLogger(name=name)

    fmt = kwargs.pop('formatter', None)
    stream = kwargs.pop('stream', sys.stdout)
    propagate = bool(kwargs.pop('propagate', True))
    #
    logger = logging.getLogger(name=name)
    logger.setLevel(level)
    hdlr = logging.StreamHandler(stream=stream)
    hdlr.setLevel(level)
    if fmt is not None:
        hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    logger.propagate = propagate
    return logger


def fixture_json(
        name: str,
        level: int,
        loop: asyncio.AbstractEventLoop,  # @UnusedVariable
        **kwargs
) -> logging.Logger:
    '''
    Json logger constructor
    :param name: logger name
    :param level: logging level
    :param loop: event loop
    :return: logger with Json format
    '''
    if has_logger_by_name(name):
        return logging.getLogger(name=name)

#     logger = logging.getLogger(name=name)
#     logger.setLevel(level)
#     fmt = SyncJsonFormatter(serializer=serializer, **extra)
#     for hdlr in logger.handlers:
#         if isinstance(hdlr, logging.StreamHandler):
#             hdlr.setLevel(level)
#             hdlr.setFormatter(fmt)
#             break
#     else:
#         hdlr = logging.StreamHandler(stream=sys.stdout)
#         hdlr.setLevel(level)
#         hdlr.setFormatter(fmt)
#         logger.addHandler(hdlr)
#     if throw_identity_warning:
#         logger.warning(
#             'logger %s re-initialized' % name,
#             extra=dict(logging_identity_warning=True)
#         )
#     return logger

    extra = kwargs.pop('extra', {})
    serializer = kwargs.pop('serializer', json.dumps)
    fmt = kwargs.pop('formatter', None)
    stream = kwargs.pop('stream', sys.stdout)
    propagate = bool(kwargs.pop('propagate', True))
    #
    logger = logging.getLogger(name=name)
    logger.setLevel(level)
    if fmt is None:
        fmt = SyncJsonFormatter(serializer=serializer, **extra)
    hdlr = logging.StreamHandler(stream=stream)
    hdlr.setLevel(level)
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    logger.propagate = propagate
    return logger


# def my_shutdown(handlerList=logging._handlerList):
#     for name in logging.Logger.manager.loggerDict:  # @UndefinedVariable
#         lg = logging.getLogger(name=name)
#         print(lg, lg.handlers)
#     for wr in reversed(handlerList[:]):
#         #errors might occur, for example, if files are locked
#         #we just ignore them if raiseExceptions is not set
#         try:
#             h = wr()
#             if h:
#                 try:
#                     print('close ', h)
#                     h.acquire()
#                     h.flush()
#                     h.close()
#                     print('closed', h)
#                 except (OSError, ValueError):
#                     # Ignore errors which might be caused
#                     # because handlers have been closed but
#                     # references to them are still around at
#                     # application exit.
#                     pass
#                 finally:
#                     h.release()
#         except: # ignore everything, as we're shutting down
#             if logging.raiseExceptions:
#                 raise
#             #else, swallow


class JanusLogger(object):
    '''
    Janus logger
    '''
    def __init__(
            self,
            name: str=__name__,
            level: int=logging.WARNING,
            loop: asyncio.AbstractEventLoop=None,
            fixture: typing.Callable[..., logging.Logger]=None,
            **kwargs
    ) -> None:
        '''
        Constructor
        :param name: name of the logger
        :param level: logging level
        :param loop: event loop
        :param fixture: logging fixture for logger
        '''
        if loop is None:
            loop = asyncio.get_event_loop()
        if fixture is None:
            fixture = fixture_default

        self.name = name

        self._extra = kwargs.pop('extra', {})
        self._level = level
        self._loop = loop
        self._log = fixture(name, level, loop, **kwargs)

    def shutdown(self) -> None:
        '''
        Shutdown logging
        '''
        logging.shutdown()

        # my_shutdown()

        # use call soon, once we use here a true async logger.
#         res = asyncio.ensure_future(
#             self._loop.run_in_executor(
#                 None,
#                 # logging.shutdown,
#                 my_shutdown
#             )
#         )

    def logger_async(self, **kwargs) -> AsyncLoggerAdapter:
        '''
        Get async logger
        :return: async logger
        '''
        return AsyncLoggerAdapter(
            self._log,
            {**self._extra, **kwargs},
            self._loop
        )

    def logger_sync(self, **kwargs) -> SyncLoggerAdapter:
        '''
        Get sync logger
        :return: sync logger
        '''
        return SyncLoggerAdapter(self._log, {**self._extra, **kwargs})
