#!/usr/bin/env python
# stats.py
# Using Python 2.7.12

import io
import sys

langs = [u'Eng', u'Spn', u'NamedEnt']

def main(argv):
	lines = []

	if len(sys.argv) == 2:
		f = io.open(argv[0], "r", encoding="utf8").readlines()
		lines = [x.strip() for x in f]
	else:
		for line in sys.stdin:
			lines.append(line.strip())

	lines = [x.split() for x in lines]
	lines = [x for x in lines if x[0] in langs]

	# Better way to do this?
	goldlist = [x[0] for x in lines]
	taglist = [x[1] for x in lines]
	nentlist = [x[2] for x in lines]

	TP = "TP"
	FN = "FN"
	FP = "FP"
	TN = "TN"

	counts = {tag : { TP : 0, FN : 0, FP : 0, TN : 0 } for tag in set(goldlist)}

	# Lang 1
	for (gold, tag) in zip(goldlist, taglist):
		if gold == "Eng":
			if tag == "Eng":
				counts[langs[0]][TP] += 1
			else:
				counts[langs[0]][FN] += 1
		else:
			if tag == "Eng":
				counts[langs[0]][FP] += 1
			else:
				counts[langs[0]][TN] += 1

	print counts

	# Lang 2
	for (gold, tag) in zip(goldlist, taglist):
		if gold == "Spn":
			if tag == "Spn":
				counts[langs[1]][TP] += 1
			else:
				counts[langs[1]][FN] += 1
		else:
			if tag == "Spn":
				counts[langs[1]][FP] += 1
			else:
				counts[langs[1]][TN] += 1

	print counts

	# Named Entities
	for (gold, nent) in zip(goldlist, nentlist):
		if gold == "NamedEnt":
			if nent != "O":
				counts[langs[2]][TP] += 1
			else:
				counts[langs[2]][FN] += 1
		else:
			if nent != "O":
				counts[langs[2]][FP] += 1
			else:
				counts[langs[2]][TN] += 1

	print counts

	# Accuracy = (TP + TN)/(TP + TN + FP + FN)
	# Precision = TP/(TP + FP)
	# Recall = TP/(TP + FN)
	accEng = counts["Eng"][TP] + counts["Eng"][TN]
	accEng = accEng / float(counts["Eng"][FP] + counts["Eng"][FN] + accEng)

	precEng = counts["Eng"][TP] / float(counts["Eng"][TP] +
			counts["Eng"][FP])

	recEng = counts["Eng"][TP] / float(counts["Eng"][TP] +
			counts["Eng"][FN])

	print "Eng: Accuracy {}, Precision {}, Recall {}".format(accEng,
			precEng, recEng)

	
	accSpn = counts["Spn"][TP] + counts["Spn"][TN]
	accSpn = accSpn / float(counts["Spn"][FP] + counts["Spn"][FN] + accSpn)

	precSpn = counts["Spn"][TP] / float(counts["Spn"][TP] +
			counts["Spn"][FP])

	recSpn = counts["Spn"][TP] / float(counts["Spn"][TP] +
			counts["Spn"][FN])

	print "Spn: Accuracy {}, Precision {}, Recall {}".format(accSpn,
			precSpn, recSpn)

	

	accNent = counts["NamedEnt"][TP] + counts["NamedEnt"][TN]
	accNent = accNent / float(counts["NamedEnt"][FP] + counts["NamedEnt"][FN] + accNent)

	precNent = counts["NamedEnt"][TP] / float(counts["NamedEnt"][TP] +
			counts["NamedEnt"][FP])

	recNent = counts["NamedEnt"][TP] / float(counts["NamedEnt"][TP] +
			counts["NamedEnt"][FN])

	print "NamedEnt: Accuracy {}, Precision {}, Recall {}".format(accNent,
			precNent, recNent)

if __name__ == "__main__":
	main(sys.argv[1:])
