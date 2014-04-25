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
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from mock import MagicMock
import gs.cache.decorator

value = 'value'


class FauxCache(object):
    '''A fake cache, for testing the decorator'''
    def __init__(self):
        self.getHit = True

    def get(self, *args):
        retval = None
        if self.getHit:
            retval = value + '-cache'
        return retval


class TestDecorator(TestCase):
    @staticmethod
    def cache_key(*args):
        return 'key'

    def test_decorator_cache_miss(self):
        '''Test the decorator when there is a cache-miss'''
        global hasRun

        f = FauxCache()
        f.getHit = False  # Set the faux-cache up to miss
        f.set = MagicMock()
        gs.cache.decorator.get_cache = MagicMock(return_value=f)

        hasRun = False

        @gs.cache.decorator.cache('test-cache', self.cache_key)
        def fn(*args):
            global hasRun
            hasRun = True
            return value

        r1 = fn()
        # The fn should be run on a cache-miss.
        self.assertTrue(hasRun)
        # The value should be set in the cache.
        self.assertEqual(1, f.set.call_count)
        args, var_args = f.set.call_args
        self.assertIn('key', args[0])
        self.assertEqual(value, args[1])
        self.assertIs(None, args[2])
        # The right value should be returned.
        self.assertEqual(value, r1)

    def test_decorator_cache_hit(self):
        '''Test the decorator on a cache-hit.'''
        global hasRun

        f = FauxCache()
        f.getHit = True
        f.set = MagicMock()
        gs.cache.decorator.get_cache = MagicMock(return_value=f)

        hasRun = False

        @gs.cache.decorator.cache('test-cache', self.cache_key)
        def fn(*args):
            global hasRun
            hasRun = True
            return value

        r1 = fn()
        # If the cache is hit then the fn should not be run.
        self.assertFalse(hasRun)
        # If the cache is hit then nothing in the cache should be set
        self.assertEqual(0, f.set.call_count)
        # The value from the cache should be returned.
        self.assertEqual(value + '-cache', r1)
