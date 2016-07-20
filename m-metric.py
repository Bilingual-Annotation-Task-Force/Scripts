#!/usr/bin/env python
# m-metric.py
# Using Python 2.7.12

import io
import sys

langs = [u'Eng', u'Spn']

def main(argv):
	tags = []

	if len(sys.argv) == 2:
		f = io.open(argv[0], "r", encoding="utf8").readlines()
		tags = [x.strip() for x in f]
	else:
		for line in sys.stdin:
			tags.append(line.strip())

	tags = [x for x in tags if x in langs]

	k = len(langs)
	total = len(tags)
	lang0 = [x for x in tags if x == langs[0]]
	lang1 = [x for x in tags if x == langs[1]]

	p0 = (len(lang0) / float(total)) ** 2
	p1 = (len(lang1) / float(total)) ** 2
	pj2 = p0 + p1
	metric = (1 - pj2) / ((k - 1) * pj2)
	
	print "M-metric: {}".format(metric)

if __name__ == "__main__":
	main(sys.argv[1:])
