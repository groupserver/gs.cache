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
from unittest import TestCase
from mock import MagicMock
import gs.cache.backends
import gs.cache.getcache
import gs.cache.interfaces


class TestGetCache(TestCase):

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
        gs.cache.getcache.redis = MagicMock()
        r = gs.cache.getcache.get_cache('testcache')
        isCache = gs.cache.interfaces.ICache.providedBy(r)
        self.assertTrue(isCache)
        self.assertIsInstance(r, gs.cache.backends.RedisCache)
