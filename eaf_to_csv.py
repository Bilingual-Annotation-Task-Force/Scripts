#!/usr/bin/env python

# using Python 2.7.13
# Written March 4th, 2017
# Last updated March 31st, 2017

# This script converts a .eaf file to a .csv file, under the following assumptions:
    ## The .eaf file has a list of time slots in <ANNOTATION_DOCUMENT><TIME_ORDER>
    ## The desired tokens are in the <TIER> element of <ANNOTATION_DOCUMENT> that has
    ##     LINGUISTIC_TYPE_REF set to "Words"
    ## The desired language annotations are in the <TIER> element that has
    ##     LINGUISTIC_TYPE_REF set to "Language"
    ## Each language annotation has ANNOTATION_REF set equal to a corresponding
    ##     ANNOTATION_ID value in the <TIER> element with LINGUISTIC_TYPE_REF set to "Syntax"


import xml.etree.cElementTree as ET
import sys
import io

def main(argv):
    assert '.eaf' in argv[0]
    output = io.open(argv[0].replace('.eaf', '.csv'), "w+")
    print "Checking file " + str(argv[0]) + "..."
    tree = ET.parse(argv[0]);
    root = tree.getroot()

    timeorder   = None # <TIME_ORDER> node
    words       = None # <TIER> node with LINGUISTIC_TYPE_REF="Words"
    syntax      = None # <TIER> node with LINGUISTIC_TYPE_REF="Syntax"
    language    = None # <TIER> node with LINGUISTIC_TYPE_REF="Language"
    
    timestamps  = [] # ordered list of timestamps
    wordmap     = {} # map from timestamps to words
    syntaxmap   = {} # map from timestamps to annotation IDs
    languagemap = {} # map from annotation IDs to languages
    
    # set up all node references first
    for child in root:
        if child.tag == 'TIME_ORDER':
            timeorder = child
        elif child.tag == 'TIER':
            if child.attrib['LINGUISTIC_TYPE_REF'] == 'Words':
                words = child
            elif child.attrib['LINGUISTIC_TYPE_REF'] == 'Syntax':
                syntax = child
            elif child.attrib['LINGUISTIC_TYPE_REF'] == 'Language':
                language = child

    if not (timeorder and words and syntax and language):
		if not timeorder:
			print "Missing TIME_ORDER section."
		if not words:
			print "Missing LINGUISTIC_TYPE_REF=\"Words\" tier."
		if not syntax:
			print "Missing LINGUISTIC_TYPE_REF=\"Syntax\" tier."
		if not language:
			print "Missing LINGUISTIC_TYPE_REF=\"Language\" tier."
		
		print "One of the needed sections seems to be missing. Terminating."
		sys.exit()
    else:
        print "Found everything. Ready to start parsing."
    
    # set up array of time stamps (ex. ts2305)
    for child in timeorder:
        if child.tag == 'TIME_SLOT':
            timestamps.append(child.attrib['TIME_SLOT_ID'])
    
    # set up dictionary mapping time stamps to words
    for child in words:
        if child.tag == 'ANNOTATION':
            for subchild in child:
                if subchild.tag == 'ALIGNABLE_ANNOTATION':
                    for subsubchild in subchild: # assuming tag ANNOTATION_VALUE
                        wordmap[subchild.attrib['TIME_SLOT_REF1']] = subsubchild.text.encode('utf8');
    
    # set up dictionary mapping timestamps to annotation IDs
    for child in syntax:
        if child.tag == 'ANNOTATION':
            for subchild in child:
                if subchild.tag == 'ALIGNABLE_ANNOTATION':
                    syntaxmap[subchild.attrib['TIME_SLOT_REF1']] = subchild.attrib['ANNOTATION_ID']
    
    # set up dictionary mapping annotation IDs to languages
    for child in language:
        if child.tag == 'ANNOTATION':
            for subchild in child:
                if subchild.tag == 'REF_ANNOTATION':
                    for subsubchild in subchild: # assuming tag ANNOTATION_VALUE
                        languagemap[subchild.attrib['ANNOTATION_REF']] = subsubchild.text;
                        
    # Man, Python is weird with Unicode
    def safe_unicode(obj): # borrowed from http://stackoverflow.com/a/34543139
        try:
            return unicode(obj)
        except UnicodeDecodeError:
            # obj is byte string
            ascii_text = str(obj).encode('string_escape')
            return unicode(ascii_text)
    
    def printoutput(): # print to the csv file
        output.write(safe_unicode(wordmap[timestamp]).decode('unicode-escape'))
        output.write(("\t" + current_language + "\n").decode())
    
    # finally, do the actual processing of timestamps and output the words and language tags to the csv file
    current_language = None # to remember which language was encoutered last
    thrown_away = 0
    numtimestamps = 0
    numwords = 0
    numlangchanges = 0
    
    print "Generating output..."
    for timestamp in timestamps:
        numtimestamps += 1
        if timestamp in wordmap: # there is a word at this time point
            numwords += 1
            if timestamp in syntaxmap and syntaxmap[timestamp] in languagemap: # we have a clause change at this point
                numlangchanges += 1
                current_language = languagemap[syntaxmap[timestamp]]
                printoutput()
            elif current_language: # we have a language
                printoutput()
            else:
                thrown_away += 1
    
    print "Finished."
    print "Words thrown away at beginning due to not having a language tag: " + str(thrown_away)
    print "Number of timestamps processed: " + str(numtimestamps)
    print "Number of words found: " + str(numwords)
    print "Number of clause/language changes: " + str(numlangchanges)

if __name__ == "__main__":
    main(sys.argv[1:])