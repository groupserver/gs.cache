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
# This code has test cases in tests/test_cache.py.
# Modifications without a supporting test case will be rejected.
#
from __future__ import absolute_import, unicode_literals
from logging import getLogger
log = getLogger('gs.cache')
import sys
if (sys.version_info >= (3, )):
    from pickle import dumps, loads
else:
    from cPickle import dumps, loads  # lint:ok
from threading import RLock
from zope.interface.declarations import implementer
from .interfaces import ICache


@implementer(ICache)
class NullCache(object):

    def __init__(self, backend=None, cache_name=None):
        return

    def set(self, key, object, expiry=None):
        """ Don't set anything, since we don't actually cache. """

    def has_key(self, key):
        """ Since we don't cache, we don't have any keys. """
        return False

    def get(self, key):
        return None

    def keys(self):
        return []

    def delete(self, key):
        return

    def clear(self):
        return


@implementer(ICache)
class RedisCache(object):
    __thread_lock = RLock()

    def __init__(self, backend, cache_name):
        self.backend = backend
        self.cache_name = cache_name

    def set(self, key, object, expiry=None):
        try:
            if not self.__thread_lock.acquire(False):
                m = "Cache ({0}), not adding object ({1}) to cache, would "\
                    "have required blocking".format(self.cache_name, key)
                log.info(m)
                return False
            fullKey = self.cache_name + '%' + key
            self.backend.set(fullKey, dumps(object))
            if expiry:
                self.backend.expire(fullKey, expiry)
        finally:
            try:
                self.__thread_lock.release()
            except:
                pass

        return True

    def has_key(self, key):
        fullKey = self.cache_name + '%' + key

        result = False
        if self.backend.keys(fullKey):
            result = True

        return result

    def get(self, key):
        fullKey = self.cache_name + '%' + key
        result = self.backend.get(fullKey)

        obj = None
        if result:
            obj = loads(result)
        return obj

    def delete(self, key):
        fullKey = self.cache_name + '%' + key
        self.backend.delete(fullKey)

    def keys(self):
        offset = len(self.cache_name) + 1
        outkeys = []
        search_string = self.cache_name + '%*'
        for key in self.backend.keys(search_string):
            outkeys.append(key[offset:])

        return outkeys

    def clear(self):
        search_string = self.cache_name + '%*'
        for key in self.backend.keys(search_string):
            self.backend.delete(key)
