#!/usr/bin/env python3
# lang_metrics.py
# Using Python 3.4.3

import os
import re
from unicodedata import normalize

# Save both name files with UTF-8 encoding

with open(r"C:\Users\Rozen\Desktop\SpanishInTexas\all_names_given.txt") as given_names:
    given_lines = given_names.read().split()

with open(r"C:\Users\Rozen\Desktop\SpanishInTexas\all_names_original.txt") as original_names:
    original_lines = original_names.read().split()

my_dict = {}

for (original_line, given_line) in zip(original_lines, given_lines):
    my_dict[original_line] = given_line

directory = r"C:\Users\Rozen\Desktop\SpanishInTexas\Spanish-in-Texas-srt\srt"

os.chdir(directory)
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:

        with open(filename) as f:
            f1 = f.read()

        output = open(directory + r"\Result\\" + filename, 'w')

        for i, j in my_dict.items():
            f1 = re.sub(r"\b" + i + r"\b", j, f1)

        print(output, f1)
        output.close()

print("finish")
