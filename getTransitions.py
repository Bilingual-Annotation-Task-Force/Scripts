#!/usr/bin/env python
# getTransitions.py
# Using Python 2.7.11

import io
import sys
from collections import Counter

langs = [u'Eng', u'Spn']

def main(argv):
	tags = []

	if len(sys.argv) >= 2:
		f = io.open(argv[0], "r", encoding="utf8").readlines()
		tags = [x.strip() for x in f]
	else:
		for line in sys.stdin:
			tags.append(line.strip())

	tags = [x for x in tags if x in langs]
	transitions = {tag : {} for tag in set(tags)}
	counts = Counter(zip(tags, tags[1:]))

	total = len(tags) - 1

	for (x, y), c in counts.iteritems():
		transitions[x][y] = c / float(total)
		print "{} -> {} : {} : {}".format(x, y, transitions[x][y], c)
	
	switchProb = 0.0
	stayProb = 0.0

	for k, v in transitions.iteritems():
		for k1, v1 in v.iteritems():
			if k == k1:
				stayProb += v1
			else:
				switchProb += v1

	print "Probability of switching language: {}".format(switchProb)
	print "Probability of maintaining language: {}".format(stayProb)

	print transitions

if __name__ == "__main__":
	main(sys.argv[1:])
