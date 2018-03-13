#!/usr/bin/env python3
# tag_translator.py
# Using Python 3.4.3
#
# PURPOSE: Convert between tagsets defined in spreadsheet file(s)


import sys
import string
import argparse

TAG_DICT = 0
POSCOL = 0
DELIMITER = 0
INFILE = 0
OUTFILE = 0
VERBOSE = False


def main(argc, argv):
    tags = {}

    # Read in tag mapping
    for line in TAG_DICT:
        mapping = line.split(DELIMITER)
        tags[mapping[0]] = mapping[1].strip()

    if VERBOSE:
        print("Tags: {}".format(tags))
        print()

    for line in INFILE:
        old_row = line.split(DELIMITER)
        old_tag = old_row[POSCOL].strip()

        new_tag = ""
        if old_tag in tags:
            new_tag = tags[old_tag]
        else:
            new_tag = ""

        new_row = old_row
        new_row[POSCOL] = new_tag
        new_row[-1] = new_row[-1].strip()

        OUTFILE.write("\t".join(new_row))
        OUTFILE.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description=("Convert between tagsetes defined in spreadsheet file(s)"))

    # Optional arguments
    parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="verbose flag (Default: False)")
    parser.add_argument(
            "-d", "--delimiter",
            type=str,
            default="\t",
            help="delimiter for input file (Default: tab)")
    parser.add_argument(
            "-c", "--column",
            metavar="n",
            type=int,
            default=1,
            help=("pos-tag column in input file "
                "(Default: 1)"))

    # Positional arguments
    parser.add_argument(
            "tag_dict",
            type=argparse.FileType("r"),
            help="Tag Mapping file")
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
            help="re-tagged file (Default: stdout)")

    args = parser.parse_args()

    if args.verbose:
        VERBOSE = True

    DELIMITER = args.delimiter
    INFILE = args.infile
    TAG_DICT = args.tag_dict
    POSCOL = args.column
    OUTFILE = args.outfile

    main(len(sys.argv), sys.argv)

    args.infile.close()
    args.outfile.close()
