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
import sys
if (sys.version_info >= (3, )):
    from pickle import dumps
else:
    from cPickle import dumps  # lint:ok
from unittest import TestCase
from mock import MagicMock
import gs.cache.backends


class TestRedis(TestCase):

    def setUp(self):
        b = MagicMock()
        self.cacheName = 'test-cache'
        self.redisBackend = gs.cache.backends.RedisCache(b, self.cacheName)

    def test_set(self):
        key = 'Ethyl'
        val = 'The Frog'
        self.redisBackend.backend.set = MagicMock()
        self.redisBackend.set(key, val)
        self.assertEqual(1, self.redisBackend.backend.set.call_count)
        args, kw_args = self.redisBackend.backend.set.call_args
        self.assertIn(key, args[0])
        self.assertIn(self.cacheName, args[0])
        self.assertEqual(dumps(val), args[1])

    def test_has_key(self):
        key = 'Ethyl'
        self.redisBackend.backend.keys = MagicMock(return_value=True)
        self.redisBackend.has_key(key)  # lint:ok
        self.assertEqual(1, self.redisBackend.backend.keys.call_count)
        args, kw_args = self.redisBackend.backend.keys.call_args
        self.assertIn(key, args[0])
        self.assertIn(self.cacheName, args[0])

    def test_get(self):
        key = 'Ethyl'
        val = 'The Frog'
        self.redisBackend.backend.get = MagicMock(return_value=dumps(val))
        r = self.redisBackend.get(key)
        self.assertEqual(val, r)
        self.assertEqual(1, self.redisBackend.backend.get.call_count)
        args, kw_args = self.redisBackend.backend.get.call_args
        self.assertIn(key, args[0])
        self.assertIn(self.cacheName, args[0])

    def test_delete(self):
        key = 'Ethyl'
        self.redisBackend.backend.delete = MagicMock()
        self.redisBackend.delete(key)
        self.assertEqual(1, self.redisBackend.backend.delete.call_count)
        args, kw_args = self.redisBackend.backend.delete.call_args
        self.assertIn(key, args[0])
        self.assertIn(self.cacheName, args[0])

    def test_keys(self):
        self.redisBackend.backend.keys = MagicMock(return_value=[])
        self.redisBackend.keys()
        self.assertEqual(1, self.redisBackend.backend.keys.call_count)
        args, kw_args = self.redisBackend.backend.keys.call_args
        self.assertIn(self.cacheName, args[0])
