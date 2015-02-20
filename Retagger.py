#This code modifies a language identified gold standard from a 2-tag system (Eng|Span) to a 3-tag system(Eng|Span|Other)

#INPUT csv file with TOKEN, POS, LANG
	##Lang = Eng | Span
	##delimiter= ,  quotechar= "
#OUTPUT csv with TOKEN, POS, Lang
	##Lang = Eng | Span | Other
	##delimiter= ,  quotechar= "
	##file name = input_file_name + "-retagged"

###USER input###
#select directory
directory = "/Users/jacqueline/Google Drive/Bullock Serigos Toribio/Bilingual Annotation/Data/"
#select input file (must be within the directory)
input_filename = "Solorio_GoldSt_7k.csv"

import os
import csv
from string import punctuation
import codecs


#change directory
os.chdir(directory)
#name for output file
output_filename = input_filename.replace(".csv", "-retagged.csv")

with open(input_filename, 'rU') as input, open(output_filename, 'wb') as output:
	corpus_input = csv.reader(input, delimiter=',', quotechar='"', dialect=csv.excel_tab)
	corpus_output = csv.writer(output, delimiter=',', quotechar='"')
	for row in corpus_input:
		if row[0] in punctuation:
			row[2] = "Other"
		if row[0].startswith("est"):
			for x in row:
				print x.decode("utf-8")
		corpus_output.writerow(row)


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


###only successful printing of text in terminal
#save excel file as UTF 16 txt file
#open with: f = codecs.open("/Users/jacqueline/Desktop/Solorio_GoldSt_7k.txt", encoding = "latin_1").readlines()
