#!/usr/bin/env python
# counts.py
# Using Python 2.7.11

import io
import sys
import math
from itertools import groupby
import numpy as np
import matplotlib.pyplot as plt

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
	Enghist = [y for (x, y) in counts if x == "Eng"]
	Spnhist = [y for (x, y) in counts if x == "Spn"]
	bins = np.linspace(0, 100, 100)
	counts = sorted([(c, len(list(cgen))) for c, cgen in groupby(counts)])
	print counts

	maxFreq = max(z for ((x, y), z) in counts)
	upperylim = int(math.ceil(maxFreq / 100.0)) * 100
	longestSpan = max(y for ((x, y), z) in counts)
	upperxlim = int(math.ceil(longestSpan / 10.0)) * 10
	
	fig = plt.figure(figsize=(8, 6))

	sub1 = fig.add_subplot(211)
	sub1.set_title("Eng Spans")
	sub1.hist(Enghist, bins)
	sub1.set_ylim([0, upperylim])
	sub1.set_xticks(np.arange(upperxlim, step=1), minor=True)
	sub1.set_xlim([0, upperxlim])
	sub1.plot()

	sub2 = fig.add_subplot(212)
	sub2.set_title("Spn Spans")
	sub2.hist(Spnhist, bins)
	sub2.set_ylim([0, upperylim])
	sub2.set_xticks(np.arange(upperxlim, step=1), minor=True)
	sub2.set_xlim([0, upperxlim])
	sub2.plot()

	plt.show()

if __name__ == "__main__":
	main(sys.argv[1:])
