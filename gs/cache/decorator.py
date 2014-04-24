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
from .getcache import get_cache


def cache(cachename, cachekeyfunc, expiry=None):
    # complex as it looks, this is the main cache decorator
    def cache_decorator(f):
        def do_cache(*args):
            cache = get_cache(cachename)
            cache_key = cachekeyfunc(*args)
            result = cache.get(cache_key)
            if not result:
                result = f(*args)
                cache.set(cache_key, result, expiry)
            return result  # do_cache
        return do_cache  # cache_decorator
    return cache_decorator  # simplecache
