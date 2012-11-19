# -*- encoding: utf-8 -*-

import os
import unittest
import shutil
import random
from utils import read_classification_from_file
from test_readClassificationFromFile import (
    create_classification,
    save_classification_to_file)
from test_corpus import (
    create_corpus_dictionary, 
    create_corpus_dir_from_dictionary)

CORPUS_DIR = 'corpus_for_testing_delete_me'
HAM_TAG = 'OK'
SPAM_TAG = 'SPAM'
TRUTH_FILENAME = '!truth.txt'
PREDICTION_FILENAME = '!prediction.txt'


class BaseFilterTestCase(unittest.TestCase):
    """Base class for all tests on various filters.
    
    The idea is to extract all the common code to this class. The concrete 
    test classes for individual filters will probably just instantiate the 
    right filter and store it in the self.filter variable.
    """
    
    def setUp(self):
        # Try to cleanup after the previous unsuccessful run if needed
        self.delete_testing_corpus()
        # ... and create a new one.
        self.create_corpus_without_truth()        
        # The following variable shall contain the filter instance to be 
        # tested. It must be set in the derived classes.
        self.filter = None
        
    def delete_testing_corpus(self):
        """Remove the corpus created for testing purposes."""
        shutil.rmtree(CORPUS_DIR, ignore_errors=True)
    
    def create_corpus_without_truth(self):
        """Create fake directory with text files for testing purposes."""
        # Create contents of the fake corpus and store them in a member 
        # variable just for the case it is needed by the add_truth_to_corpus.
        self.file_dict = create_corpus_dictionary()
        create_corpus_dir_from_dictionary(self.file_dict, CORPUS_DIR)
        
    def tearDown(self):
        self.delete_testing_corpus()

    def test_trainMethod(self):
        """Filter method train() shall run quietly. 
        
        Smoke test. Does not assert anything, just tries to run the method.
        """
        # Prepare the SUT
        # The train() method may use the !truth.txt file, create it!
        self.add_truth_to_corpus()
        # Excercise the SUT
        self.filter.train(CORPUS_DIR)
        # Nothing to assert, if we got this far, declare success
        
    def add_truth_to_corpus(self):
        """Add a truth file to the existing fake corpus."""
        d = {key: random.choice([HAM_TAG, SPAM_TAG]) 
             for key in self.file_dict.keys()}
        self.truth_filepath = os.path.join(CORPUS_DIR, TRUTH_FILENAME)
        save_classification_to_file(d, self.truth_filepath)        

    def test_testMethod(self):
        """Verify that test() method creates the !prediction.txt file."""

        # Exercise SUT
        self.filter.test(CORPUS_DIR)
        # Verify
        self.assertPredictionFileExistsAndContainsClassificationFor(self.file_dict)

    def assertPredictionFileExistsAndContainsClassificationFor(self, expected):
        fpath = os.path.join(CORPUS_DIR, PREDICTION_FILENAME)
        self.assertTrue(os.path.isfile(fpath),
            "The test() method did not create the !prediction.txt file.")
        observed = read_classification_from_file(fpath)
        self.assertEqual(
            sorted(expected.keys()), sorted(observed.keys()),
            'The !prediction.txt file does not contain decisions for the files it should.')
        self.assertTrue(
            all(value in (SPAM_TAG,HAM_TAG) for value in observed.values()))
        
    def test_trainAndTest(self):
        """Execute the train() and test() methods in a sequence as in real use."""
        # Prepare the SUT
        # The train() method may use the !truth.txt file, create it!
        self.add_truth_to_corpus()
        # Excercise the SUT
        self.filter.train(CORPUS_DIR)
        # Before testing, delete the !truth.txt file
        os.unlink(self.truth_filepath)
        # Test the filter on the same corpus
        self.filter.test(CORPUS_DIR)
        # Verify
        self.assertPredictionFileExistsAndContainsClassificationFor(self.file_dict)
        