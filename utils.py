import os

def read_classification_from_file(filename):
	""" Return { <filename> : <classification> } dict """
	with open(filename, "rt") as f:
		classification = {}
		
		for line in f:
			key, value = line.split()
			classification[key] = value

		return classification