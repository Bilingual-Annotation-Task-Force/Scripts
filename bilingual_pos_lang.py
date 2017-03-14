#!/usr/bin/env python3
# bilingual_pos_lang.py
# Using Python 3.4.3
#
# PURPOSE: Compute transitions of POS tags and languages

import sys
import argparse
from collections import Counter

POSCOL = 0
LANGCOL = 1
DELIMITER = "\t"
HEADER = False
VERBOSE = False
INFILE = 0
OUTFILE = 0


def main(argc, argv):
    tags = get_tags()
    tag_counts = Counter(zip(tags, tags[1:]))

    # Generate transition matrix of POS tags
    for (tag1, tag2), count in tag_counts.items():
        pos1, lang1 = tag1
        pos2, lang2 = tag2
        OUTFILE.write("{}\t{}\t{}\t{}\t{}\n".format(lang1, lang2, pos1, pos2, count))


def get_tags():
        tags = []
        pos_tags = []
        lang_tags = []

        # Read all tags
        for line in INFILE:
                pos_tag = line.split(DELIMITER)[POSCOL]
                pos_tags.append(pos_tag.strip())
                lang_tag = line.split(DELIMITER)[LANGCOL]
                lang_tags.append(lang_tag.strip())

        # Skip first line if header specified
        if HEADER:
                lang_tags = lang_tags[1:]
                pos_tags = pos_tags[1:]

        # Combine in one list
        tags = list(zip(pos_tags, lang_tags))

        # Print working set of language tags if needed
        if VERBOSE:
                print("Set of POS tags: {}".format(set(pos_tags)))
                print("Set of language tags: {}".format(set(lang_tags)))

        return tags


if __name__ == "__main__":
        parser = argparse.ArgumentParser(
                description="Compute transitions of POS tags and languages")

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
                metavar=("col1", "col2"),
                nargs=2,
                default=[0, 1],
                help=("POS-tag and language columns in input file "
                      "(Default: 0-1)"))
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
        POSCOL = int(args.columns[0])
        LANGCOL = int(args.columns[1])
        OUTFILE = args.outfile

        main(len(sys.argv), sys.argv)

