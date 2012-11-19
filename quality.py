import os
from confmat import BinaryConfusionMatrix
from utils import read_classification_from_file

def quality_score(tp, tn, fp, fn):
	""" Compute score, where FP is ten times worse than FN """
	return (tp + tn) / (tp + tn + 10 * fp + fn)

def compute_quality_for_corpus(corpus_dir):
	""" Compute quality_score() for predictions in corpus """
	matrix = BinaryConfusionMatrix(pos_tag="SPAM", neg_tag="OK")

	matrix.compute_from_dicts(
		dict(read_classification_from_file(os.path.join(corpus_dir, "!truth.txt"))),
		dict(read_classification_from_file(os.path.join(corpus_dir, "!prediction.txt")))
	)

	return quality_score(**matrix.as_dict())