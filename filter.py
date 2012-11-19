import os
import math
import re
from collections import Counter

def read_classification_from_file(filename):
	""" Return { <filename> : <classification> } dict """
	with open(filename, "rt") as f:
		classification = {}
		
		for line in f:
			key, value = line.split()
			classification[key] = value

		return classification

def read_files(dir):
	""" ( <filename>, <content> ) generator """
	for filename in os.listdir(dir):
		if filename[0] == "!": continue
		with open(dir + "/" + filename, "rt") as f:
			yield filename, f.read()

class MyFilter:
	""" Simple bayesian-based spam filter """

	def __init__(self):
		self.spams = Counter()
		self.hams = Counter()
		self.spamicity = {}
		self.regexp = re.compile(r"(?:(?:\w+(?:\.\w+)*@)?(?:[a-zA-Z0-9_]+\.)+[a-z]{2,12})|[a-zA-Z0-9]+")

	def __tokenize(self, s):
		""" Return list of tokens for given string """
		return [ word.lower() for word in self.regexp.findall(s) if len(word) < 30]

	def train(self, dir):
		""" Train filter with classified data """
		classification = read_classification_from_file(dir + "/!truth.txt")
		spam_total = 0
		ham_total = 0

		for id, message in read_files(dir):
			cls = classification[id]

			if cls == "SPAM":
				spam_total += 1
			else:
				ham_total += 1

			for word in set(self.__tokenize(message)):
				if cls == "SPAM":
					self.spams[word] +=1
				else:
					self.hams[word] += 1

		spam_probability = spam_total / (spam_total + ham_total)
		ham_probability = 1 - spam_probability

		for word in (set(self.spams.keys()) | set(self.hams.keys())):
			self.spamicity[word] = (self.spams[word] / spam_total * spam_probability) / \
				(self.spams[word] / spam_total * spam_probability + self.hams[word] / ham_total * ham_probability)

	# good defaults, measured on test data
	EASING = 0.095
	SLICING = 38

	def test(self, dir):
		""" Run filter """
		with open(dir + "/!prediction.txt", "wt") as f:
			for id, message in read_files(dir):
				a, b = 1.0, 1.0

				for word, spamicity in                                                            \
						sorted(                                                                   \
							[ (w, 0.5 if self.spamicity.get(w) == None else self.spamicity[w])    \
								for w in self.__tokenize(message) ],                              \
							key=lambda x: 0.5 - math.fabs(0.5 - x[1])                             \
						)[0:self.SLICING]:

					a *= math.fabs(spamicity - self.EASING)
					b *= 1.0 - spamicity + self.EASING


				f.write(id + " " + ("SPAM" if (a / (a + b)) >= 1.0 else "OK") + "\n")
