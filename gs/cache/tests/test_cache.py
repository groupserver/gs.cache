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
##############################################################################
from __future__ import absolute_import, unicode_literals
import time
from unittest import main, TestSuite, makeSuite, TestCase
from mock import MagicMock
import gs.cache.backends
import gs.cache.getcache
import gs.cache.interfaces


class GetCacheTest(TestCase):

    def setUp(self):
        gs.cache.getcache.caches = {}  # Because of the cache of caches

    def test_get_null_cache(self):
        gs.cache.getcache.haveredis = False
        gs.cache.getcache.get_backend = MagicMock(return_value='none')
        r = gs.cache.getcache.get_cache('testcache')
        isCache = gs.cache.interfaces.ICache.providedBy(r)
        self.assertTrue(isCache)
        self.assertIsInstance(r, gs.cache.backends.NullCache)

    def test_get_redis_cache(self):
        gs.cache.getcache.haveredis = True
        gs.cache.getcache.get_backend = MagicMock(return_value='redis')
        r = gs.cache.getcache.get_cache('testcache')
        isCache = gs.cache.interfaces.ICache.providedBy(r)
        self.assertTrue(isCache)
        self.assertIsInstance(r, gs.cache.backends.RedisCache)

    def foo_test_set(self):
        test_key = 'blargkey'
        test_value = 'blargvalue'

        haskey = test_key in self.tcache
        assert not haskey

        self.tcache.set(test_key, test_value)
        value = self.tcache.get(test_key)
        assert value == test_value

        haskey = test_key in self.tcache
        assert haskey

        keys = list(self.tcache.keys())
        assert len(keys) == 1
        self.tcache.clear()
        keys = list(self.tcache.keys())
        assert len(keys) == 0

    def foo_test_setexpiry(self):
        test_key = 'blargexpirykey'
        test_value = 'blargexpiryvalue'

        haskey = test_key in self.tcache
        assert not haskey

        self.tcache.set(test_key, test_value, 2)
        value = self.tcache.get(test_key)
        assert value == test_value

        haskey = test_key in self.tcache
        assert haskey

        time.sleep(3)

        haskey = test_key in self.tcache
        assert not haskey

        keys = list(self.tcache.keys())
        assert len(keys) == 0


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(GetCacheTest))
    return suite

if __name__ == '__main__':
    main(defaultTest='test_suite')
