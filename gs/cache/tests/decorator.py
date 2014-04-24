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


class FauxCache(object):
    '''A fake cache, for testing the decorator'''
    def __init__(self):
        self.getHit = True

    def get(self, *args):
        retval = None
        if self.getHit:
            retval = 'value'
        return retval


class TestDecorator(TestCase):
    @staticmethod
    def cache_key(*args):
        return 'key'

    def test_decorator_cache_miss(self):
        global hasRun

        f = FauxCache()
        f.getHit = False
        f.set = MagicMock()
        gs.cache.decorator.get_cache = MagicMock(return_value=f)

        hasRun = False

        @gs.cache.decorator.cache('test-cache', self.cache_key)
        def fn(*args):
            global hasRun
            hasRun = True
            return 'value'

        r1 = fn()
        self.assertTrue(hasRun)
        self.assertEqual(1, f.set.call_count)
        self.assertEqual('value', r1)

    def test_decorator_cache_hit(self):
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
            return 'value'

        r1 = fn()
        self.assertFalse(hasRun)
        self.assertEqual(0, f.set.call_count)
        self.assertEqual('value', r1)
