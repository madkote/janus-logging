janus-logging
=============
.. image:: https://travis-ci.com/madkote/janus.svg?branch=master
    :target: https://travis-ci.com/madkote/janus
.. image:: https://codecov.io/gh/madkote/janus/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/madkote/janus
.. image:: https://img.shields.io/pypi/v/janus.svg
    :target: https://pypi.python.org/pypi/janus-logging
.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/aio-libs/Lobby
    :alt: Chat on Gitter

sync and async logging within one logger instance.

Installation
------------

.. code:: sh

    pip install janus-logging

Usage
-----

Default
~~~~~~~

.. code:: python

    import asyncio
    import logging
    import sys

    import janus_logging

    def threaded(sync_log, counter: int):
        for i in range(counter):
        sync_log.info('s-Hello #%s' % i)
        sync_log.info('s-Finished #%s' % counter)

    async def async_coro(async_log, counter: int):
        for i in range(counter):
        await async_log.info('aio-Hello #%s' % i)
        await async_log.info('aio-Finished #%s' % counter)

    #
    counter = 4
    name = 'my_janus_logger'
    level = logging.DEBUG
    stream = sys.stdout
    loop = asyncio.get_event_loop()
    #
    logger = janus_logging.JanusLogger(name=name, level=level, loop=loop, stream=stream)
    loop.run_until_complete(
        asyncio.gather(
        loop.run_in_executor(
            None,
            threaded,
            logger.logger_sync(),
            counter
        ),
        async_coro(
            logger.logger_async(),
            counter
        )
        )
    )
    logger.shutdown()
    #
    #
    loop.close()

The output of above will look like:

.. code:: sh

    s-Hello #0
    s-Hello #1
    s-Hello #2
    aio-Hello #0
    s-Hello #3
    s-Finished #4
    aio-Hello #1
    aio-Hello #2
    aio-Hello #3
    aio-Finished #4

Please note, that the output might be different on your instance.

JSON
~~~~

Simply use *fixtures*.

.. code:: python

    import asyncio
    import logging
    import sys

    import janus_logging

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

    #
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

The output of above will look like:

.. code:: sh

    {"bla": "blabla", "logger_name": "logger_sync", "counter": 0, "log_type": "sync", "log_status": "in progress", "logged_at": "2019-09-27T12:00:02.517101+02:00", "line_numer": 35, "function": "threaded", "level": "INFO", "msg": "s-Hello #0", "file_path": "demo_janus_log.py"}
    {"logged_at": "2019-09-27T12:00:02.518000+02:00", "line_number": 60, "function": "info", "level": "INFO", "file_path": "/home/madkote/janus-logging/janus_logging/__init__.py", "msg": "aio-Hello #1", "bla": "blabla", "logger_name": "logger_async", "counter": 1, "log_type": "async", "log_status": "in progress"}
    ...

Custom
~~~~~~

If a custom loggeer, formatter, handler are required, then create custom
*fixtures* and pass them to the ``JanusLogger``.

.. code:: python

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

    logger = janus_logging.JanusLogger(
        ...,
        fixture_async=fixture_async_default,
        fixture_sync=custom_fixture_sync,
        ...
    )

Development
-----------

Issues and suggestions are welcome through *issues*
