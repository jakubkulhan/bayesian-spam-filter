#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test the Corpus class."""

import os
import shutil
import unittest
from test_readClassificationFromFile import (
    random_filename, 
    random_string,
    FNAME_CHARS)

from corpus import Corpus

SPECIAL_FILENAME = '!special.txt'
CORPUS_DIR = 'testing_corpus_delete_me'
FCONTENTS_CHARS = FNAME_CHARS + '\n '
N_EMAILS = 20

class TestCorpus(unittest.TestCase):

    def setUp(self):
        """Prepare classification file for the test."""
        self.expected = create_corpus_dictionary(N_EMAILS)
        create_corpus_dir_from_dictionary(self.expected)
    
    def tearDown(self):
        delete_corpus_directory()
        
    def test_corpusContainsOnlyEmails(self):
        """Test reading the corpus with email messages only."""
        corpus = Corpus(CORPUS_DIR)
        # Exercise the SUT
        observed = {}
        for fname, contents in corpus.emails_as_string():
            observed[fname] = contents
        # Verify the results
        self.assertEqual(len(self.expected), len(observed),
                         'The emails_as_string() method did not generate all the corpus files.')
        self.assertEqual(self.expected, observed,
                             'The read file contents are not equal to the expected contents.')
        
    def test_corpusContainsAlsoSpecialFiles(self):
        """Test reading the corpus with special files."""
        # Add a special file into the corpus dir
        save_file_to_corpus_dir(
            fname=SPECIAL_FILENAME, contents='fake', dirname=CORPUS_DIR)     
        corpus = Corpus(CORPUS_DIR)
        # Exercise the SUT
        observed = {}
        for fname, contents in corpus.emails_as_string():
            observed[fname] = contents
        # Verify the results
        self.assertEqual(len(self.expected), len(observed),
                         'The emails_as_string() method did not generate all the corpus files.')
        self.assertEqual(self.expected, observed,
                             'The read file contents are not equal to the expected contents.')

def create_corpus_dictionary(nitems=N_EMAILS):
    """Create a random dictionary of email file names and their contents."""
    d = {}
    for i in range(nitems):
        filename = random_filename()
        contents = random_string(200, chars=FCONTENTS_CHARS)
        d[filename] = contents
    return d

def create_corpus_dir_from_dictionary(d, dirname=CORPUS_DIR):
    """Save the dictionary to a directory."""
    os.makedirs(dirname, exist_ok=True)
    for fname, contents in d.items():
        save_file_to_corpus_dir(fname, contents, dirname)
    
def save_file_to_corpus_dir(fname, contents, dirname=CORPUS_DIR):
    """Save the contents to the file into the dirname directory."""
    fpath = os.path.join(dirname, fname)
    with open(fpath, 'wt', encoding='utf-8') as f:
        f.write(contents)
        
def delete_corpus_directory(dirname=CORPUS_DIR):
    """Delete the directory with testing corpus."""
    shutil.rmtree(dirname, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
