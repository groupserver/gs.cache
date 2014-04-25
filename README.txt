============
``gs.cache``
============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A shared cache between processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-04-25
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
`the Redis data structure server`_. If Redis is unavailable a
null-cache is used.

The `gs.cache.cache`_ decorator is the main mechanism for using
the cache. Simpler non-persistent per-thread caches can be
created using ``zope.cachedescriptors`` [#zcd]_.

.. _the Python redis module: http://pypi.python.org/pypi/redis/
.. _the redis data structure server: http://redis.io/

``gs.cache.cache``
==================

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
  The optional expiry date, in seconds, for items in the cache
  (``int``).

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

The example below [#list]_ shows the use of ``gs.cache.cache``
decorator. The function ``gs.dmarc.lookup_receiver_policy`` is
slow, because it has to make a DNS request to retrieve the DMARC
policy for a site [#dmarc]_. To mitigate this issue a cache is
added::

    @gs.cache.cache('Products.XWFMailingList.dmarc', lambda s, h: h, 7 * 60)
    def get_dmarc_policy_for_host(self, host):
        retval = gs.dmarc.lookup_receiver_policy(host)
        return retval

To add a cache the original ``lookup_receiver_policy`` function
is wrapped in ``get_dmarc_policy_for_host`` [#static]_. This
function is decorated with ``gs.cache.cache``.

* The cache-name is ``Products.XWFMailingList.dmarc``.
* The function to generate the cache-key is a lambda-function. It
  takes the same two arguments as the wrapped function (``self``,
  and ``host``) and returns the second as the key (``host``).
* Because DMARC policy settings can change a cache-timeout of
  seven minutes (``7 * 60`` seconds) is set.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.cache/
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#zcd] For more information on ``zope.cachedescriptors`` see
          <https://pypi.python.org/pypi/zope.cachedescriptors>
.. [#list] The example is taken from
           ``Products.XWFMailingListManager.XWFMailingList``.
.. [#dmarc] For more information on ``gs.dmarc`` see
            <https://source.iopen.net/groupserver/gs.dmarc/>.
.. [#static] The **actual** ``get_dmarc_policy_for_host`` method
             is a static-method. This results in a
             double-decorator, so the function declaration
             actually looks like the following::

               @staticmethod
               @cache('Products.XWFMailingList.dmarc', lambda h: h, 7 * 60)
               def get_dmarc_policy_for_host(host):

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

..  LocalWords:  redis
