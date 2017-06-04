#!/usr/bin/env python3
# pangloss_xml_to_tsv.py
# Using Python 3.4.3
#
"""Convert Pangloss XML files to TSV format"""

import xml.etree.ElementTree as EleTree

import sys
import argparse

VERBOSE = False
INFILE = 0
OUTFILE = 0


def main():
    OUTFILE.write("Token\tSentence\tTranslation\tLanguage\n")

    tree = EleTree.parse(INFILE)
    root = tree.getroot()

    for s in root.findall("./S"):
        sentence = s.attrib["id"]
        for m in s.findall("./W/M"):
            token = m.findtext("FORM")
            trans = m.findtext("TRANSL")

            if m.attrib:
                lang = m.attrib["class"]
            else:
                lang = "L"

            OUTFILE.write("{}\t{}\t{}\t{}\n".format(token, sentence, trans, lang))


if __name__ == "__main__":
    global VERBOSE, INFILE, OUTFILE

    parser = argparse.ArgumentParser(
        description="Convert Paris XML files to TSV format")

    # Optional arguments
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="verbose flag")
    parser.add_argument(
        "-i", "--in-place",
        action="store_true",
        help="write to file of same name as input")

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
        help="output file (Default: stdout)")

    args = parser.parse_args()

    if args.verbose:
        VERBOSE = True

    INFILE = args.infile
    OUTFILE = args.outfile

    if args.in_place and INFILE.name != "<stdin>":
        filename = args.infile.name.split(".")[0]
        OUTFILE = open(filename + ".tsv", "wt")

    main()

    args.infile.close()
    args.outfile.close()
