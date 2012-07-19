#
# This code has test cases in tests/test_cache.py.
# Modifications without a supporting test case will be rejected.
#

from zope.interface.declarations import implements
from zope.interface import Interface
from threading import RLock
from cPickle import dumps, loads
from gs.config import Config, getInstanceId
from gs.cache.backends import NullCache, RedisCache
import datetime
import logging
log = logging.getLogger('gs.cache')

try:
    import redis
    haveredis = True
except ImportError:
    haveredis = False

class BackendError(Exception):
    pass

caches = {}
def get_cache(cache_name, instance_id=None):
    if not instance_id:
        instance_id = getInstanceId()

    # prepend the cache_name with the instance_id to make it unique across
    # instances
    cache_name = instance_id+"::"+cache_name

    # yes, we have a cache of caches :-)
    if caches.has_key(cache_name):
        return caches[cache_name]

    config = Config(instance_id)
    config.set_schema('cache', {'backend': str, 'hostname': str, 'port': int})
    cache_config = config.get('cache')
    
    backend = cache_config.get('backend', 'none')
    
    if backend == 'redis' and haveredis:
        redisCache = redis.StrictRedis(host='localhost', port=6379, db=0)
        caches[cache_name] = RedisCache(redisCache, cache_name)
    elif backend == 'none':
        caches[cache_name] = NullCache()    
    else:
        raise BackendError(u'No cache backend implemented for "%s"' % backend)

    log.info(u'Intialising cache "%s" using backend "%s"' % (cache_name,backend))
    
    return caches[cache_name]

# complex as it looks, this is the main cache decorator
def cache(cachename, cachekeyfunc, expiry=None):
    def cache_decorator(f):
        def do_cache(*args):
            cache = get_cache(cachename)
            cache_key = cachekeyfunc(*args)
            result = cache.get(cache_key)
            if not result:
                result = f(*args)
                cache.set(cache_key, result, expiry)
            
            return result # do_cache

        return do_cache # cache_decorator

    return cache_decorator # simplecache
