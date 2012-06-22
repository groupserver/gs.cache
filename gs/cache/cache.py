#
# This code has test cases in tests/test_cache.py.
# Modifications without a supporting test case will be rejected.
#

from zope.interface.declarations import implements
from zope.interface import Interface
import datetime

import redis

from threading import RLock

from cPickle import dumps, loads

import logging
log = logging.getLogger('XWFCore.cache')

redisCache = redis.StrictRedis(host='localhost', port=6379, db=0)

class ICache(Interface):
    def set(key, object): #@NoSelf
        """ Add an object to the cache.
        
        """
        
    def has_key(key): #@NoSelf
        """ Check to see if an object is in the cache.
        
        """
        
    def get(key): #@NoSelf
        """ Get an object from the cache by key.
        
        """

    def remove(key): #@NoSelf
        """ Remove an object from the cache by key.

        """
        
    def clear(): #@NoSelf
        """Clear all instances from a cache
        """

def cache(cachename, cachekeyfunc, expiry=None):
    def cache_decorator(f):
        def do_cache(*args):
            cache = SimpleCache(redisCache, cachename)
            cache_key = cachekeyfunc(*args)
            result = cache.get(cache_key)
            if not result:
                result = f(*args)
                cache.set(cache_key, result, expiry)
            
            return result # do_cache

        return do_cache # cache_decorator

    return cache_decorator # simplecache

class SimpleCache(object):
    """ Implement ICache with no expiry.
    
    """
    implements(ICache)
    __thread_lock = RLock()
    
    def __init__(self, backend, cache_name):
        self.backend = backend
        self.cache_name = cache_name
        
    def set(self, key, object, expiry=None):
        try:
            if not self.__thread_lock.acquire(False):
                log.info("Cache (%s), not adding object (%s) to cache, would have required blocking" % (self.cache_name, key))
                return False
            fullKey = self.cache_name+'%'+key
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
        fullKey = self.cache_name+'%'+key
        
        result = False
        if self.backend.keys(fullKey):
            result = True
        
        return result        

    def get(self, key):
        fullKey = self.cache_name+'%'+key
        result = redisCache.get(fullKey)
        
        object = None
        if result:
            object = loads(result)        

        return object 

    def delete(self, key):
        fullKey = self.cache_name+'%'+key
        redisCache.delete(fullKey)    

    def keys(self):
        offset = len(self.cache_name)+1
        outkeys = []
        search_string = self.cache_name+'%*'
        for key in self.backend.keys(search_string):
            outkeys.append(key[offset:])
        
        return outkeys
 
    def clear(self):
        search_string = self.cache_name+'%*'
        for key in self.backend.keys(search_string):
            self.backend.delete(key)
