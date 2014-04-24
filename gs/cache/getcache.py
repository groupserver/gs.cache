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


caches = {}


def get_backend(instance_id=None):
    config = Config(instance_id)
    config.set_schema('cache', {'backend': str, 'hostname': str, 'port': int})
    cache_config = config.get('cache')

    retval = cache_config.get('backend', 'none')
    return retval


def get_cache(cache_name, instance_id=None):
    if not instance_id:
        instance_id = getInstanceId()

    # prepend the cache_name with the instance_id to make it unique across
    # instances
    cache_name = instance_id + "::" + cache_name

    # yes, we have a cache of caches :-)
    if cache_name in caches:
        return caches[cache_name]

    backend = get_backend(instance_id)

    if backend == 'redis' and haveredis:
        redisCache = redis.StrictRedis(host='localhost', port=6379, db=0)
        caches[cache_name] = RedisCache(redisCache, cache_name)
    elif backend == 'none':
        caches[cache_name] = NullCache()
    else:
        raise BackendError('No cache backend implemented for "%s"' % backend)

    log.info('Intialising cache "%s" using backend "%s"' % (cache_name,
                                                                backend))

    return caches[cache_name]
