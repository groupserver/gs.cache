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
from zope.interface import Interface


class ICache(Interface):

    def set(key, object):
        """ Add an object to the cache.

        """

    def has_key(key):
        """ Check to see if an object is in the cache.

        """

    def get(key):
        """ Get an object from the cache by key.

        """

    def remove(key):
        """ Remove an object from the cache by key.

        """

    def clear():
        """Clear all instances from a cache
        """
