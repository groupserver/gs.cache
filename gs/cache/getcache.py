# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
###############################################################################
#
# This code has test cases in tests/test_cache.py.
# Modifications without a supporting test case will be rejected.
#
from __future__ import absolute_import, unicode_literals
import logging
log = logging.getLogger('gs.cache')
try:
    import redis
    haveredis = True
except ImportError:
    haveredis = False
from gs.config import Config, getInstanceId
from .backends import NullCache, RedisCache


class BackendError(Exception):
    pass


# Yes, we have a cache of caches :-)
caches = {}


def get_backend(instance_id=None):
    '''Get the cache configuration information.'''
    config = Config(instance_id)
    config.set_schema('cache', {'backend': str, 'hostname': str, 'port': int})
    cache_config = config.get('cache')

    retval = cache_config.get('backend', 'none')
    return retval


def get_cache(cache_name, instance_id=None):
    '''Get the cache for the current instance.'''
    if not instance_id:
        instance_id = getInstanceId()

    # prepend the cache_name with the instance_id to make it unique across
    # instances
    cache_name = instance_id + "::" + cache_name

    # Add the cache to the cache of caches.
    if cache_name in caches:
        return caches[cache_name]

    backend = get_backend(instance_id)

    # --=mpj17=-- TODO: Replace with named adaptors
    if backend == 'redis' and haveredis:
        # TODO: Get the host, port and db from the config file.
        redisCache = redis.StrictRedis(host='localhost', port=6379, db=0)
        caches[cache_name] = RedisCache(redisCache, cache_name)
    elif backend == 'none':
        caches[cache_name] = NullCache()
    else:
        raise BackendError('No cache backend implemented for "%s"' % backend)

    m = 'Intialising cache "{0}" using backend "{1}".'
    msg = m.format(cache_name, backend)
    log.info(msg)

    return caches[cache_name]
