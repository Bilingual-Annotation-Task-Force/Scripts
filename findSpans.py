#!/usr/bin/env python
# counts.py
# Using Python 2.7.11

import sys
import io
from itertools import groupby

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
	counts = sorted([(c, len(list(cgen))) for c, cgen in groupby(tags)])
	counts = sorted([(c, len(list(cgen))) for c, cgen in groupby(counts)])

	print counts

if __name__ == "__main__":
	main(sys.argv[1:])
