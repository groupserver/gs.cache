============
``gs.cache``
============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Shared cache between processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-04-24
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

Introduction
============

A GroupServer system may be served by multiple threads running in
multiple Zope processes; having an external *shared* cache allows
every thread maintain a consistent state. The ``gs.cache``
product provides this caching mechanism. Behind the scenes `the
Python redis module`_ is used to store the key-value pairs in
`the redis data structure server`_.

The `cache decorator`_ is the main mechanism for using the
cache. Simpler per-thread caches can be gained by using
``zope.cachedescriptors`` [#zcd]_.

.. _the Python redis module: http://pypi.python.org/pypi/redis/
.. _the redis data structure server: http://redis.io/

Cache decorator
===============

Lazily evaluate a function, storing the result in a shared cache.

Synopsis
--------

::

  @gs.cache.cache(cacheName, cacheKeyFunc, [expiry])
  def some_function(…):

Description
-----------

The ``gs.cache.cache`` function decorator adds multi-thread
caching to a function. The ``cacheKeyFunction`` is evaluated to
generate a key. Then the cache (possibly stored using Redis)
specified by ``cacheName`` is checked for the key. If present the
value stored in the cache is returned. Otherwise the decorated
function is evaluated, the returned value stored in the cache
(under the cache key), and returned.

Arguments
---------

``cacheName``:
  The name of the cache to store the results in (``str``).

``cacheKeyFunc``:
  A function to generate the cache-key. It will be passed the
  same arguments ast the decorated function.

``expiry``:
  The optional expiry date (``datetime.datetime``).

Returns
-------

* The value of the decorated function if the cache-key returned
  by ``cacheKeyFunc`` is absent from the cache specified by
  ``cacheName``.
* The value pointed to by ``cacheKeyFunc`` in the cache specified
  by ``cacheName`` if there is a value stored in the cache.

Side effects
------------

On a cache-miss the decorated function is evaluated. The value
returned by the decorated function is stored in the cache under
the value specified by the cache-key.

Example
-------

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.cache/
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#zcd] See <https://pypi.python.org/pypi/zope.cachedescriptors>

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

..  LocalWords:  redis
