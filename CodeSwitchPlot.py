#!/usr/bin/env python
# CodeSwitchPlot.py
# Using Python 2.7.11

import sys
import io
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt

# Tags to convert to 1 or -1
valid_tags = ["Eng", "Spn"]

# Default smooth value
default_smooth = 5

def main(argv):
	goldTags = io.open(argv[0], 'r', encoding='utf8').readlines()
	smooth = int(argv[1]) if len(sys.argv) >= 3 else default_smooth
	tags = [x.strip() for x in goldTags]
	tags = tags[:1000] # Add default slice values?
	num_tags = [1 if x == valid_tags[0] else -1 for x in tags]
	N = len(num_tags)
	T = 1/float(N) # Assuming regular sampling
	x = np.linspace(0.0, N, N)
	x2 = np.linspace(0.0, N/2, N)
	y = num_tags
	w = scipy.fftpack.rfft(y)
	f = scipy.fftpack.rfftfreq(N, x[1] - x[0])
	w[0] = 0
	spectrum = w**2
	cutoff_idx = spectrum < (spectrum.max() / smooth)
	w2 = w.copy()
	w2[cutoff_idx] = 0
	y2 = scipy.fftpack.irfft(w2)

	step = N/50
	fig = plt.figure(figsize=(15, 10))

	sub1 = fig.add_subplot(311) # Better way to display switches?
	sub1.set_title('Switches')
	sub1.plot(x, y)
	sub1.set_ylim([-1.5, 1.5])
	sub1.set_xlim([0, N])
	ticks = sub1.set_yticklabels(['', valid_tags[1], '', '', '', valid_tags[0], ''])
	sub1.set_xticks(np.arange(N/2, step=step), minor=True)
	sub1.plot(x, np.zeros(N), linestyle='dashed')

	sub2 = fig.add_subplot(323, axisbg='lightgrey') # Normalize FFT?
	sub2.set_title('FFT of switches')
	sub2.set_xticks(np.arange(N/2, step=step/2), minor=True)
	sub2.plot(x2, w**2)

	sub3 = fig.add_subplot(324) # What is a good cutoff?
	sub3.set_title('Smoothed FFT')
	sub3.set_xticks(np.arange(100, 2), minor=True)
	sub3.set_xlim([0, 100])
	sub3.plot(x2, w2**2)

	sub4 = fig.add_subplot(313) # ???
	sub4.set_title('Smoothed Switches')
	sub4.set_xticks(np.arange(N/2, step=step), minor=True)
	sub4.set_xlim([0, N])
	sub4.plot(x, y2)

	plt.show()

if __name__ == "__main__":
	main(sys.argv[1:])
