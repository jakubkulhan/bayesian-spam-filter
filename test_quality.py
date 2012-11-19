import unittest
import os
import shutil
from confmat import BinaryConfusionMatrix
from test_readClassificationFromFile import (
    create_classification, 
    save_classification_to_file)

from quality import (
    quality_score,
    compute_quality_for_corpus)

class QualityScoreTest(unittest.TestCase):
    
    def test_qualityScore_return1_ifConfmatContainsTpOnly(self):
        # Prepare fixture
        cm_dict = {'tp': 100, 'tn': 0, 'fp': 0, 'fn': 0}
        # Exercise the SUT
        q = quality_score(**cm_dict)
        # Assertions
        self.assertEqual(q, 1.0)

    def test_qualityScore_return1_ifConfmatContainsTnOnly(self):
        # Prepare fixture
        cm_dict = {'tp': 0, 'tn': 100, 'fp': 0, 'fn': 0}
        # Exercise the SUT
        q = quality_score(**cm_dict)
        # Assertions
        self.assertEqual(q, 1.0)

    def test_qualityScore_return1_ifCconfmatContainsTpOrTnOnly(self):
        # Prepare fixture
        cm_dict = {'tp': 100, 'tn': 100, 'fp': 0, 'fn': 0}
        # Exercise the SUT
        q = quality_score(**cm_dict)
        # Assertions
        self.assertEqual(q, 1.0)
        
    def test_qualityScore_return0_ifConfmatContainsFpOnly(self):
        # Prepare fixture
        cm_dict = {'tp': 0, 'tn': 0, 'fp': 100, 'fn': 0}
        # Exercise the SUT
        q = quality_score(**cm_dict)
        # Assertions
        self.assertEqual(q, 0.0)

    def test_qualityScore_return0_ifConfmatContainsFnOnly(self):
        # Prepare fixture
        cm_dict = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 100}
        # Exercise the SUT
        q = quality_score(**cm_dict)
        # Assertions
        self.assertEqual(q, 0.0)

    def test_qualityScore_return0_ifConfmatContainsFpOrFnOnly(self):
        # Prepare fixture
        cm_dict = {'tp': 0, 'tn': 0, 'fp': 100, 'fn': 100}
        # Exercise the SUT
        q = quality_score(**cm_dict)
        # Assertions
        self.assertEqual(q, 0.0)

    def test_qualityScore_whenConfmatHasAllCountersEqual(self):
        """
        Here we assume the quality function in the form:
        q = (tp + tn) / (tp + tn + 10*fp + fn)
        """
        # Prepare fixture
        cm_dict = {'tp': 1, 'tn': 1, 'fp': 1, 'fn': 1}
        # Exercise the SUT
        q = quality_score(**cm_dict)
        # Assertions
        self.assertEqual(q, 2/13)

CORPUS_DIR = 'corpus_for_testing_delete_me'
TRUTH_FILENAME = '!truth.txt'
PREDICTION_FILANAME = '!prediction.txt'
SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'

class ComputeQualityForCorpusTest(unittest.TestCase):

    def setUp(self):
        # Create a corpus directory
        os.makedirs(CORPUS_DIR, exist_ok=True)
        
    def tearDown(self):
        # Delete the corpus directory
        shutil.rmtree(CORPUS_DIR, ignore_errors=True)
    
    def test_allPredictionsCorrect(self):
        # Prepare the SUT
        create_identical_truth_and_prediction_file()
        # Excercise the SUT
        q = compute_quality_for_corpus(CORPUS_DIR)
        # Assertions
        self.assertEqual(q, 1.0)
        
    def test_allPredictionsWrong(self):
        # Prepare the SUT
        create_inverse_truth_and_prediction_file()
        # Excercise the SUT
        q = compute_quality_for_corpus(CORPUS_DIR)
        # Assertions
        self.assertEqual(q, 0.0)
        
def create_identical_truth_and_prediction_file():
    """
    Create identical !truth.txt and !prediction.txt files in the corpus directory.

    Here we assume that the corpus directory already exists.
    """
    # Create an artificial email classification dictionary  
    class_dict = create_classification()
    # Compile the filepaths
    truth_filepath = os.path.join(CORPUS_DIR, TRUTH_FILENAME)
    pred_filepath = os.path.join(CORPUS_DIR, PREDICTION_FILANAME)
    # Save the same dictionary as both the !truth.txt and !prediction.txt
    save_classification_to_file(class_dict, truth_filepath)
    save_classification_to_file(class_dict, pred_filepath)

def create_inverse_truth_and_prediction_file():
    """
    Create inverse !truth.txt and !prediction.txt files in the corpus directory.

    Here we assume that the corpus directory already exists.
    """
    # Create an artificial truth dictionary
    truth_dict = create_classification()
    # Create an inverted version of truth_dict
    pred_dict = invert_classes(truth_dict)
    # Compile the filepaths
    truth_filepath = os.path.join(CORPUS_DIR, TRUTH_FILENAME)
    pred_filepath = os.path.join(CORPUS_DIR, PREDICTION_FILANAME)
    # Save the dictionaries in !truth.txt and !prediction.txt, respectively.
    save_classification_to_file(truth_dict, truth_filepath)
    save_classification_to_file(pred_dict, pred_filepath)

def invert_classes(orig_dict):
    """Return a dict with switched HAM_TAG and SPAM_TAG."""
    inv_dict = {}
    for email_filename, truth in orig_dict.items():
        inv_dict[email_filename] = \
            SPAM_TAG if truth==HAM_TAG else HAM_TAG
    return inv_dict
    
if __name__=='__main__':
    unittest.main()