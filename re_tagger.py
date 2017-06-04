#!/usr/bin/env python3
# re_tagger.py
# Using Python 3.5.2

"""This code modifies a language identified gold standard from
        a 2-tag system (Eng|Span) to a 3-tag system(Eng|Span|Other)
    Punctuation

    INPUT csv file with TOKEN, POS, LANG
        Lang = Eng | Span
        delimiter= ','
        quotechar= '"'
        dialect = csv.excel_tab
    OUTPUT csv with TOKEN, POS, Lang
        Lang = Eng | Span | Other
        delimiter= ','
        quotechar= '"'
        default dialect = csv.excel_tab
        file name = input_file_name - ".csv" + "-retagged.csv"
"""

import os
import csv
from string import punctuation

# select directory
TARGET_DIR = "/Users/jacqueline/Google Drive/Bullock Serigos Toribio/Bilingual Annotation/Data/"
# select input file (must be within the directory)
INPUT_FILENAME = "Solorio_GoldSt_7k.csv"


if __name__ == "__main__":
    # change directory
    os.chdir(TARGET_DIR)
    # name for output file
    output_filename = INPUT_FILENAME.replace(".csv", "-retagged.csv")

    with open(INPUT_FILENAME, 'rU') as infile, open(output_filename, 'wb') as outfile:
        corpus_input = csv.reader(infile, delimiter=',', quotechar='"', dialect=csv.excel_tab)
        corpus_output = csv.writer(outfile, delimiter=',', quotechar='"')
        for row in corpus_input:
            if row[0] in punctuation:
                row[2] = "Other"
            if row[0].startswith("est"):
                for x in row:
                    print(x.decode("utf-8"))
            corpus_output.writerow(row)
