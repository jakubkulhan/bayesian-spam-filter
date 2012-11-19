import os
from random import getrandbits

def ls(dir):
	for filename in os.listdir(dir):
		if filename[0] != "!": yield filename

def save_prediction(dir, prediction):
	with open(os.path.join(dir, "!prediction.txt"), "wt") as f:
		for filename, classification in prediction.items():
			f.write(filename + " " + classification + "\n")

class BaseFilter:
	def train(self, dir):
		pass

	def test(self, dir):
		raise NotImplementedError

class NaiveFilter(BaseFilter):
	def test(self, dir):
		save_prediction(dir, dict([(filename, "OK") for filename in ls(dir)]))

class ParanoidFilter(BaseFilter):
	def test(self, dir):
		save_prediction(dir, dict([(filename, "SPAM") for filename in ls(dir)]))

class RandomFilter(BaseFilter):
	def test(self, dir):
		save_prediction(dir, dict([(filename, "SPAM" if not getrandbits(1) else "OK") for filename in ls(dir)]))
