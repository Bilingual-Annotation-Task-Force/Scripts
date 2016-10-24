#!/usr/bin/env python
# metrics.py
# Using Python 2.7.11
#
# PURPOSE: Given language-tagged data, find code switch points in the data (array "switchPoints")
# and determine how many language tags are between each switch point (array "intereventTimes").
# Then export arrays switchPoints and intereventTimes to a .csv formatted file for analysis in R, Excel

import io
import sys
import math
import csv
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
	tags = process_input(argv)
	# Return input from get_ functions according to user input at command line
		
# Read in data from input(s): instantiate an array of tags in n-tuple format,
# with n entries corresponding to the n values in each line of text/csv input
# Return 'tags', this list of tuples
def process_input(argv):
	print("not implemented")
	tags = []
	return tags

# Return m-metric
def get_m_metric(tags):
	#todo
	print("not implemented")
	m_metric = 0
	return m_metric

def get_i_metric(tags):
	#todo
	print("not implemented")
	i_metric = 0
	return i_metric

def get_spans(tags):
	#todo
	print("not implemented")
	spans = []
	return spans

def get_switch_points(tags):
	#todo
	print("not implemented")
	switch_points = []
	return switch_points

def get_burstiness(tags):
	#todo
	print("not implemented")
	burstiness = 0
	return burstiness

def get_memory(tags):
	#todo
	print("not implemented")
	memory = 0
	return burstiness