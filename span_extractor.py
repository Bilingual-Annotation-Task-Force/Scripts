#!/usr/bin/env python3
# span_extractor.py
# Using Python 3.6.2
#
# PURPOSE: Extracts language spans from tagged corpora

import sys
import argparse
from itertools import groupby
from operator import itemgetter

TOKCOL = 0
LANGCOL = 1
DELIMITER = "\t"
HEADER = False
VERBOSE = False
INFILE = 0
OUTFILE = 0


def main():
        tags = []
        tokens = []
        lang_tags = []

        # Read all tags
        for line in INFILE:
                token = line.split(DELIMITER)[TOKCOL]
                tokens.append(token.strip())
                lang_tag = line.split(DELIMITER)[LANGCOL]
                lang_tags.append(lang_tag.strip())

        # Skip first line if header specified
        if HEADER:
                tokens = tokens[1:]
                lang_tags = lang_tags[1:]

        # Combine in one list
        tags = list(zip(tokens, lang_tags))

        # Print working set of language tags if needed
        if VERBOSE:
                print("Total tokens: {}".format(len(tokens)))
                print("Set of language tags: {}".format(set(lang_tags)))

        # Convert to span format if not already
        new_tags = []
        for lang, group in groupby(tags, itemgetter(1)):
                span = [x[0] for x in group]
                new_tags.append((" ".join(span), len(span), lang))

        tags = new_tags

        # Write to file
        OUTFILE.write("Span\tLength\tLanguage\n")
        for span, length, lang in tags:
                OUTFILE.write("{}\t{}\t{}\n".format(span, length, lang))


if __name__ == "__main__":
        parser = argparse.ArgumentParser(
                description="Extracts language spans from tagged corpora")

        # Optional arguments
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
                "-c", "--columns",
                metavar=("col1", "col2"),
                nargs=2,
                default=[0, 1],
                help=("Token and language columns in input file "
                      "(Default: 0 & 1)"))
        parser.add_argument(
                "--header",
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
                help="metrics file (Default: stdout)")

        args = parser.parse_args()

        if args.verbose:
                VERBOSE = True

        if args.header:
                HEADER = True

        DELIMITER = args.delimiter
        INFILE = args.infile
        TOKCOL = int(args.columns[0])
        LANGCOL = int(args.columns[1])
        OUTFILE = args.outfile

        main()

        args.infile.close()
        args.outfile.close()
