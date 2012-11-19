import unittest

from confmat import BinaryConfusionMatrix

SPAM_TAG = 'SPAM'
HAM_TAG = 'HAM'

class BinaryConfusionMatrixTest(unittest.TestCase):
 
    def setUp(self):
        # Prepare fixture
        self.cm = BinaryConfusionMatrix(pos_tag=SPAM_TAG, neg_tag=HAM_TAG)
 
    def test_countersAreZero_afterCreation(self):
        # Exercise the SUT
        cmdict = self.cm.as_dict()
        # Assert
        self.assertDictEqual(cmdict, {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0})

    def test_updatesTPcorrectly(self):
        # Exercise the SUT
        self.cm.update(SPAM_TAG, SPAM_TAG)
        # Assert
        self.assertDictEqual(self.cm.as_dict(),
                             {'tp': 1, 'tn': 0, 'fp': 0, 'fn': 0})
        
    def test_updatesTNcorrectly(self):
        # Exercise the SUT
        self.cm.update(HAM_TAG, HAM_TAG)
        # Assert
        self.assertDictEqual(self.cm.as_dict(),
                             {'tp': 0, 'tn': 1, 'fp': 0, 'fn': 0})  
        
    def test_updatesFPcorrectly(self):
        # Exercise the SUT
        self.cm.update(HAM_TAG, SPAM_TAG)
        # Assert
        self.assertDictEqual(self.cm.as_dict(),
                             {'tp': 0, 'tn': 0, 'fp': 1, 'fn': 0})  
        
    def test_updatesFNcorrectly(self):
        # Exercise the SUT
        self.cm.update(SPAM_TAG, HAM_TAG)
        # Assert
        self.assertDictEqual(self.cm.as_dict(),
                             {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 1})
        
    def test_update_raisesValueError_forWrongTruthValue(self):
        # This test may be ignored (deleted). 
        # It tests an additional feature of the BCF class.
        
        # Assert and exercise the SUT
        with self.assertRaises(ValueError):
            self.cm.update('a bad value', SPAM_TAG)
 
    def test_update_raisesValueError_forWrongPredictionValue(self):
        # This test may be ignored (deleted). 
        # It tests an additional feature of the BCF class.
        
        # Assert and exercise the SUT
        with self.assertRaises(ValueError):
            self.cm.update(SPAM_TAG, 'a bad value')
            
    def test_computeFromDicts_allCasesOnce(self):
        # Prepare fixture
        truth = {1: SPAM_TAG,
                 2: SPAM_TAG,
                 3: HAM_TAG,
                 4: HAM_TAG}
        prediction = {1: SPAM_TAG,
                      2: HAM_TAG,
                      3: SPAM_TAG,
                      4: HAM_TAG}
        # Excercise the SUT
        self.cm.compute_from_dicts(truth, prediction)
        # Assert
        self.assertDictEqual(self.cm.as_dict(),
                             {'tp': 1, 'tn': 1, 'fp': 1, 'fn': 1})    
        
if __name__=='__main__':
    unittest.main()