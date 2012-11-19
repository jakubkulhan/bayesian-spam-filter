#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test the read_classification_from_file() function."""

import os
import unittest
import random

from utils import read_classification_from_file

FNAME_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
FILENAME = '!delete_me.txt'
HAM_TAG = 'OK'
SPAM_TAG = 'SPAM'
EMAIL_CLASSES = (HAM_TAG, SPAM_TAG)

class ReadClassificationTest(unittest.TestCase):

    def test_returnEmptyDict_forEmptyFile(self):
        # Prepare fixture
        expected = dict()
        save_classification_to_file(expected, FILENAME)
        
        # Excercise the SUT
        observed = read_classification_from_file(FILENAME)
        
        # Validate results
        self.assertDictEqual(
            expected, observed,
            'The read dictionary shall be empty for empty file.')

    def test_correctlyFormattedFile(self):
        # Prepare fixture
        expected = create_classification()
        save_classification_to_file(expected, FILENAME)
        
        # Exercise the SUT
        observed = read_classification_from_file(FILENAME)

        # Validate results
        self.assertDictEqual(
            expected, observed,
            'The read file contents are not equal to the expected contents.')
            
    def tearDown(self):
        """Delete the classification file if it exists."""
        try:
            os.unlink(FILENAME)
        except:
            pass
        
def save_classification_to_file(d, fname):
    """Save the classification dictionary to a file."""
    with open(fname, 'wt', encoding='utf-8') as f:
        for key, value in d.items():
            f.write(key + ' ' + value + '\n')
            
def create_classification(nitems=20):
    """Create a random dictionary of classified email filenames."""
    d = {}
    for i in range(nitems):
        d[random_filename()] = random.choice(EMAIL_CLASSES)
    return d

def random_filename(fnamelength=8, ext_prob=1):
    """Create a filename as a random sequance of letters and numbers, possibly with an extension."""
    fname = random_string(fnamelength)
    ext = ''
    if random.random() < ext_prob:
        ext = '.' + random_string(3)
    return fname + ext

def random_string(strlength=8, chars=FNAME_CHARS):
    """Create a string as a random sequence of the given chars."""
    sampled_chars = [random.choice(chars) for i in range(strlength)]
    return ''.join(sampled_chars)
                
if __name__ == "__main__":
    unittest.main()
