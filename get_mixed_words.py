#!/usr/bin/env python3
# get_mixed_words.py
# Using Python 3.6.5
#
# PURPOSE: Get words not present in dictionary

import sys
import aspell
import argparse

LANGS = []
LANG_TAGS = []
LANGCOL = 0
DELIMITER = "\t"
HEADER = False
VERBOSE = False
INFILE = 0
OUTFILE = 0

def main():
        global LANGS, NUMTAGS, LANG_TAGS, GROUP_TAGS

        for line in INFILE:
                lang_tag = line.split(DELIMITER)[LANGCOL]
                LANG_TAGS.append(lang_tag.strip())

        if HEADER:
                LANG_TAGS = LANG_TAGS[1:]

        lang1 = aspell.Speller('lang', LANGS[0])
        lang2 = aspell.Speller('lang', LANGS[1])

        mixed_words = set()

        for word in LANG_TAGS:
                if word not in lang1 and word not in lang2:
                        mixed_words.add(word)

        for word in mixed_words:
                OUTFILE.write(word)
                OUTFILE.write("\n")

if __name__ == "__main__":
        parser = argparse.ArgumentParser(
                description=("Get words not present in dictionary"))

        # Optional arguments
        parser.add_argument(
                "-l", "--langs",
                metavar=("lang1", "lang2"),
                nargs=2,
                default=[],
                help="languages in corpus (Default: all)")
        parser.add_argument(
                "-d", "--delimiter",
                type=str,
                default="\t",
                help="delimiter for input file (Default: tab)")
        parser.add_argument(
                "-v", "--verbose",
                action="store_true",
                help="verbose flag (Default: False)")
        parser.add_argument(
                "-c", "--column",
                metavar="n",
                type=int,
                default=0,
                help=("language column in input file "
                      "(Default: 0)"))
        parser.add_argument(
                "-H", "--header",
                action="store_true",
                help="header flag  (Default: False)")

        # Positional arguments
        parser.add_argument(
                "infile",
                nargs="?",
                type=argparse.FileType("r"),
                default=sys.stdin,
                help="corpus file (Default: stdin)")
        parser.add_argument(
                "outfile",
                nargs="?",
                type=argparse.FileType("w"),
                default=sys.stdout,
                help="mixed words file (Default: stdout)")

        args = parser.parse_args()

        if args.verbose:
                VERBOSE = True
                print(args)

        if args.header:
                HEADER = True

        DELIMITER = args.delimiter
        INFILE = args.infile
        LANGCOL = args.column
        LANGS = args.langs
        OUTFILE = args.outfile

        main()

        args.infile.close()
        args.outfile.close()

