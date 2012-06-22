from unittest import main, TestSuite, makeSuite, TestCase
from gs.cache import cache
import time

class CacheTest(TestCase):
    def setUp(self):
        self.tcache = cache.SimpleCache(cache.redisCache,
                                        'aCacheName')  
        self.tcache.clear()
        
    def tearDown(self):
        self.tcache.clear()
        
    def test_set(self):
        test_key = 'blargkey'
        test_value = 'blargvalue'
        
        haskey = self.tcache.has_key(test_key)
        assert haskey == False

        self.tcache.set(test_key, test_value)
        value = self.tcache.get(test_key)
        assert value == test_value

        haskey = self.tcache.has_key(test_key)
        assert haskey == True

        keys = self.tcache.keys()
        assert len(keys) == 1
        self.tcache.clear()
        keys = self.tcache.keys()
        assert len(keys) == 0
        
    def test_setexpiry(self):
        test_key = 'blargexpirykey'
        test_value = 'blargexpiryvalue'

        haskey = self.tcache.has_key(test_key)
        assert haskey == False

        self.tcache.set(test_key, test_value, 2)
        value = self.tcache.get(test_key)
        assert value == test_value

        haskey = self.tcache.has_key(test_key)
        assert haskey == True

        time.sleep(3)

        haskey = self.tcache.has_key(test_key)
        assert haskey == False

        keys = self.tcache.keys()
        assert len(keys) == 0

def test_suite():
   suite = TestSuite()
   suite.addTest(makeSuite(CacheTest))
   return suite

if __name__ == '__main__':
    main(defaultTest='test_suite')
