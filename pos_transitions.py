#!/usr/bin/env python3
# pos_transitions.py
# Using Python 3.4.3
#
# PURPOSE: Calculate transitions between pos-tags to describe code-switching behavior in
# pos-tagged corpora.

import sys
import argparse

TOKCOL = 0
LANGCOL = 1
POSCOL = 2
DELIMITER = "\t"
HEADER = False
VERBOSE = False
INFILE = 0
OUTFILE = 0


def main(argc, argv):
        tags = []
        tokens = []
        lang_tags = []
        pos_tags = []

        # Read all tags
        for line in INFILE:
                token = line.split(DELIMITER)[TOKCOL]
                tokens.append(token.strip())
                lang_tag = line.split(DELIMITER)[LANGCOL]
                lang_tags.append(lang_tag.strip())
                pos_tag = line.split(DELIMITER)[POSCOL]
                pos_tags.append(pos_tag.strip())

        # Skip first line if header specified
        if HEADER:
                tokens = tokens[1:]
                lang_tags = lang_tags[1:]
                pos_tags = pos_tags[1:]

        # Combine in one list
        tags = list(zip(tokens, lang_tags, pos_tags))

        # Print working set of language tags if needed
        if VERBOSE:
                print("Length of tokens: {}".format(len(tokens)))
                print("Set of language tags: {}".format(set(lang_tags)))
                print("Set of POS tags: {}".format(set(pos_tags)))

        line_bigrams = zip(tags, tags[1:])

        OUTFILE.write("Lang1\tLang2\tPOS1\tPOS2\tTOK1\tTOK2\n")

        # Compute transitions and find tokens
        for line1, line2 in line_bigrams:
            tok1, tok2 = line1[0], line2[0]
            lang1, lang2 = line1[1], line2[1]
            pos1, pos2 = line1[2], line2[2]

            OUTFILE.write("\t".join((lang1, lang2, pos1, pos2, tok1, tok2)))
            OUTFILE.write("\n")

if __name__ == "__main__":
        parser = argparse.ArgumentParser(
                description=("Compute transitions of POS tags and languages"
                            " over all tokens"))

        # Optional arguments
        parser.add_argument(
                "-d", "--delimiter",
                type=str,
                default="\t",
                help="delimiter for input file (Default: tab)")
        parser.add_argument(
                "-v", "--verbose",
                action="store_true",
                help="verbose flag")
        parser.add_argument(
                "-c", "--columns",
                metavar=("col1", "col2", "col3"),
                nargs=3,
                default=[0, 1, 2],
                help=("Token, POS-tag, and language columns in input file "
                      "(Default: 0-2)"))
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
                help="transition file (Default: stdout)")

        args = parser.parse_args()

        if args.verbose:
                VERBOSE = True

        if args.header:
                HEADER = True

        DELIMITER = args.delimiter
        INFILE = args.infile
        TOKCOL = int(args.columns[0])
        LANGCOL = int(args.columns[1])
        POSCOL = int(args.columns[2])
        OUTFILE = args.outfile

        main(len(sys.argv), sys.argv)

