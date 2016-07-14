#!/usr/bin/env python
# getTransitions.py
# Using Python 2.7.11

import sys
import io
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
from collections import Counter
import math

langs = [u'Eng', u'Spn']

def main(argv):
	tags = []
	transitions = {langs[0]: {}, langs[1]: {}}

	if len(sys.argv) >= 2:
		f = io.open(argv[0], "r", encoding="utf8").readlines()
		tags = [x.strip() for x in f]
	else:
		for line in sys.stdin:
			tags.append(line.strip())

	tags = [x for x in tags if x in langs]
	counts = Counter(zip(tags, tags[1:]))

	total = sum(counts.values()) # Get new total for language tags

	for (x, y), c in counts.iteritems(): # Compute transition matrix
		transitions[x][y] = c / float(total)
		print "{} -> {} : {} : {}".format(x, y, transitions[x][y], c)

	switchProb = transitions[langs[0]].get(langs[1], 0.0) + \
			transitions[langs[1]].get(langs[0], 0.0)
	stayProb = transitions[langs[0]].get(langs[0], 0.0) + \
			transitions[langs[1]].get(langs[1], 0.0)

	print "Probability of switching language: {}".format(switchProb)
	print "Probability of maintaining language: {}".format(stayProb)

	print transitions

if __name__ == "__main__":
	main(sys.argv[1:])
