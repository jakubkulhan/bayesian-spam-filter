import unittest
import tst_filterbase

from simplefilters import (
    NaiveFilter,
    ParanoidFilter,
    RandomFilter)

class NaiveFilterTest(tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of the NaiveFilter class for the test
        self.filter = NaiveFilter()
        
class ParanoidFilterTest(tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of the ParanoidFilter class for the test
        self.filter = ParanoidFilter()

class RandomFilterTest(tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of the RandomFilter class for the test
        self.filter = RandomFilter()
        
if __name__=='__main__':
    unittest.main(exit=False)
