Introduction
============

A GroupServer system may be served by multiple threads running in multiple
Zope processes; having an external *shared* cache allows every thread
maintain a consistent state. The ``gs.cache`` product provides the caching
mechanism. Behind the scenes `the Python redis module`_ is used to store
the key-value pairs in `the redis data structure server`_.

.. _the Python redis module: http://pypi.python.org/pypi/redis/
.. _the redis data structure server: http://redis.io/

..  LocalWords:  redis
