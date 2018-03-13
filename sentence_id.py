#!/usr/bin/env python3
# sentence_id.py
# Using Python 3.6.3
#
# PURPOSE: Calculate sentence boundaries on tagged data

import sys
import math
import argparse

SENT = []
POSCOL = 0
DELIMITER = "\t"
HEADER = False
VERBOSE = False
INFILE = 0
OUTFILE = 0

def main():
        i = 0
        s = "s"
        pos_tags = []

        for line in INFILE:
                pos_tag = line.split(DELIMITER)[POSCOL]
                pos_tags.append(pos_tag)

        # Skip first line if header specified
        if HEADER:
                pos_tags = pos_tags[1:]
                OUTFILE.write("Sentence\n")

        # Increment sentence counter every time we see a sentence end marker
        for pos_tag in pos_tags:
                if pos_tag in SENT:
                        OUTFILE.write(s + str(i) + "\n")
                        i += 1
                else:
                        OUTFILE.write(s + str(i) + "\n")

        if VERBOSE:
                print("Set of postags: {}".format(set(pos_tags)))
                print("Number of sentences: {}".format(i))
                print("Number of tokens: {}".format(len(pos_tags)))


if __name__ == "__main__":
        parser = argparse.ArgumentParser(
                description="Calculate sentence boundaries on tagged data")

        # Optional arguments
        parser.add_argument(
                "-s", "--sentence-token",
                nargs=argparse.REMAINDER,
                default=["SENT", "FS", ".", "...", "?", "!"],
                help="Sentence end markers (Default: SENT, FS, ., ..., ?, !)")
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
                default=1,
                help=("pos-tag column in input file "
                      "(Default: 1)"))
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
                help="sentencized file (Default: stdout)")

        args = parser.parse_args()

        if args.verbose:
                VERBOSE = True

        if args.header:
                HEADER = True

        DELIMITER = args.delimiter
        INFILE = args.infile
        POSCOL = args.column
        OUTFILE = args.outfile
        SENT = args.sentence_token

        main()

        args.infile.close()
        args.outfile.close()
