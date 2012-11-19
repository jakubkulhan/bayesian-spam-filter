import os

class Corpus:
	def __init__(self, dirname):
		self.dirname = dirname

	def emails_as_string(self):
		for filename in os.listdir(self.dirname):
			if filename[0] == "." or filename[0] == "!":
				continue
			with open(self.dirname + os.sep + filename, "rt") as file:
				yield filename, file.read()