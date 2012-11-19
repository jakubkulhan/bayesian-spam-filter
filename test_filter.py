#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for MyFilter class."""

import tst_filterbase

class MyFilterTest(tst_filterbase.BaseFilterTestCase):
    
    def setUp(self):
        super().setUp()
        # Set an instance of the MyFilter class for the test
        from filter import MyFilter
        self.filter = MyFilter()
       
if __name__=='__main__':
    unittest.main()