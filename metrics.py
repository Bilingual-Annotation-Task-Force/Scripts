#!/usr/bin/env python
# metrics.py
# Using Python 2.7.11
#
# PURPOSE: Calculate various metrics to describe code-switching behavior in
# language-tagged corpora.

import io
import os
import sys
import csv
import subprocess

langs = []
languageColumn = -1
delimiter = -1

def main(argv):
	taggedData = process_input(argv)
	get_m_metric(taggedData)
	get_switch_points(taggedData)
	get_burstiness_and_memory(taggedData)
	# Return input from get_ functions according to user input at command line
		
# Read in data from input(s): instantiate an array of tags in n-tuple format,
# with n entries corresponding to the n values in each line of text/csv input
# Return 'tags', this list of tuples
def process_input(argv):
	fileExtension = argv[1].split(".")[1]
	
	if(fileExtension is "xls" or fileExtension is "xlsx"):
		# Excel input
		print("Excel input not implemented")

	elif(fileExtension is csv): 
		f = io.open(argv[1], encoding="utf-8")
		reader = csv.reader(f)
		tags = [row for row in reader]

	else: # txt files
		# To do: fix broken formatting on files with inconsistent whitespace delimited values
		f = io.open(argv[1], encoding="utf-8")
		reader = csv.reader(f)
		tags = [row for row in reader]

	# Print a list of headers and prompt user to select the language-tagged column.
	for i in range(len(tags[0])):
		print(str(i+1)+") "+tags[0][i])

	global languageColumn
	languageColumn = int(input("Enter the integer corresponding to the language tagged column: "))-1

	return tags

# Return m-metric
def get_m_metric(tags):
	# Remove tags marked as punctuation, as they are not used in calculation of the m-metric.
	tags = [x for x in tags if x[languageColumn] != "Punct"]
	# Generate a list of all languages used in the corpus.
	global langs
	langCounts = []
	for x in tags[1:]:
		if x[languageColumn] not in langs:
			langs.append(x[languageColumn])
			langCounts.append(0)
	# Count how many words are in each language.
	for x in tags[1:]:
		for y in langs:
			if x[languageColumn] == y:
				langCounts[langs.index(y)] += 1

	# Print this word count for each language.
	for x in langs:
		print("Language: "+x+"\tCount: "+str(langCounts[langs.index(x)]))
	print("Total:\t"+str(sum(langCounts[:])))
	
	# Calculate the m-metric using each language's word counts.
	p = sum([(x/sum(langCounts[:]))**2 for x in langCounts])
	m_metric = (1-p)/((sum(langCounts[:])-1)*p)
	print("m-Metric: {}".format(m_metric))
	return m_metric

def get_i_metric(tags):
	#todo
	print("not implemented")
	i_metric = 0
	return i_metric

def get_spans(tags):
	# Returns a list of word distances between switch points, i.e. spans of speaking in one language
	switch_points = get_switch_points(tags)
	spans = []
	for i in range(len(switch_points)-1):
		spans.append(switch_points[i+1]-switch_points[i])
	return spans

def get_switch_points(tags):
	# Remove tags marked as punctuation, as they are not used in calculation of the m-metric.
	tags = [x for x in tags if x[languageColumn] != "Punct"]
	# Generate a list of all languages used in the corpus.
	global langs
	langCounts = []
	for x in tags[1:]:
		if x[languageColumn] not in langs:
			langs.append(x[languageColumn])
			langCounts.append(0)
	# Go through the language-tagged column and get indexes of points where
	# a language differs from the one before it.
	switch_points = []
	for i in range(len(tags)):
		if tags[i][languageColumn] != tags[i-1][languageColumn]:
			switch_points.append(i)
	return switch_points

def get_burstiness_and_memory(tags):
	# Generate a new .csv of language spans.
	spans = get_spans()
	output = open(argv[0]+"-spans.csv", 'wb')
	wr = csv.writer(output, quoting=csv.QUOTE_NONE)
	wr.writerow(["spans"])
	for i in range (len(spans)):
		wr.writerow([spans[i]])

	# Run the burstiness R script on the new .csv to get burstiness & memory info for the corpora.
	cmd = ["Rscript", os.getcwd()+"burstiness.R "+argv[0]+"-spans.csv"]
	x = subprocess.check_output(cmd, universal_newlines=True)
	print(x)
	burstiness = 0
	return burstiness

#def get_memory(tags):
#	#todo
#	print("not implemented")
#	memory = 0
#	return burstiness

if __name__ == "__main__":
	main(sys.argv[:])