class BinaryConfusionMatrix:
	""" Computes true positives, true negatives, false positives and false negatives """

	def __init__(self, pos_tag, neg_tag):
		self.pos_tag = pos_tag
		self.neg_tag = neg_tag
		self.tp, self.tn, self.fp, self.fn = 0, 0, 0, 0

	def as_dict(self):
		""" Return { tp: ..., tn: ..., fp: ..., fn: ... } """
		return { "tp": self.tp, "tn": self.tn, "fp": self.fp, "fn": self.fn }

	def update(self, truth, prediction):
		""" Update TP, TN, FP, FN counters """
		if truth not in (self.pos_tag, self.neg_tag) or prediction not in (self.pos_tag, self.neg_tag):
			raise ValueError("Only " + self.pos_tag + " or " + self.neg_tag + " allowed, " + truth + " and " + prediction + " given")

		if prediction == self.pos_tag:
			if prediction == truth:
				self.tp += 1
			else:
				self.fp += 1

		else:
			if prediction == truth:
				self.tn += 1
			else:
				self.fn += 1

	def compute_from_dicts(self, truth_dict, prediction_dict):
		""" Iterate through prediction_dict and call update() for each element """
		for key in prediction_dict:
			self.update(truth_dict[key], prediction_dict[key])