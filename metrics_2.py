#!/usr/bin/env python3
# metrics.py
# Using Python 3.4.3
#
# PURPOSE: Calculate various metrics to describe code-switching behavior in
# language-tagged corpora.

import io
import os
import sys
from collections import Counter
from itertools import groupby
import numpy as np
import math
import argparse

LANGS = []
LANGCOL = 0
DELIMITER = "\t"
HEADER = False
VERBOSE = False
INFILE = 0
OUTFILE = 0


def get_tags():
        global LANGS, LANGCOL, DELIMITER, VERBOSE

        lang_tags = []

        # Read all language tags into variable
        for line in INFILE:
                lang_tag = line.split(DELIMITER)[LANGCOL]
                lang_tags.append(lang_tag.strip())

        # Skip first if header exists
        if HEADER:
                lang_tags = lang_tags[1:]

        # Only include specific languages
        # And remove all whitespace
        lang_tags = [lang for lang in lang_tags if lang in LANGS]

        return lang_tags


def main(argv, argc):
        lang_tags = get_tags()
        m_metric = get_m_metric(lang_tags)
        i_index = get_i_index(lang_tags)
        burstiness = get_burstiness(lang_tags)
        memory = get_memory(lang_tags)

        print("M-metric: {}".format(m_metric))
        print("I-index: {}".format(i_index))
        print("Burstiness: {}".format(burstiness))
        print("Memory: {}".format(memory))


def get_m_metric(lang_tags):
        k = len(LANGS)
        total = len(lang_tags)
        lang1 = [x for x in lang_tags if x == LANGS[0]]
        lang2 = [x for x in lang_tags if x == LANGS[1]]

        p1 = (len(lang1) / float(total)) ** 2
        p2 = (len(lang2) / float(total)) ** 2
        pj = p1 + p2

        m_metric = (1 - pj) / ((k - 1) * pj)

        return m_metric


def get_i_index(lang_tags):
        switches = {lang: {} for lang in set(lang_tags)}
        counts = Counter(zip(lang_tags, lang_tags[1:]))

        total = len(lang_tags) - 1

        for (x, y), c in counts.items():
                switches[x][y] = c / float(total)

        i_index = 0.0

        for lang1, switch in switches.items():
                for lang2, prob in switch.items():
                        if lang1 != lang2:
                                i_index += prob

        return i_index


def get_burstiness(lang_tags):
        spans = get_spans(lang_tags)
        mean = np.mean(spans)
        sd = np.std(spans)

        return (sd - mean)/(sd + mean)


def get_memory(lang_tags):
        spans = get_spans(lang_tags)
        mean1 = np.mean(spans[:-1])
        mean2 = np.mean(spans[1:])
        sd1 = np.std(spans[:-1])
        sd2 = np.std(spans[1:])
        memory = 0.0

        for i, span in enumerate(spans[:-1]):
                memory +=(span - mean1) * (spans[i + 1] - mean2)

        memory /= (len(spans) - 1) * (sd1 * sd2)
                
        return memory


def get_spans(lang_tags):
        return [len(list(group)) for lang, group in groupby(lang_tags)][:-1]

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Calculate various \
                        metrics to describe CS behavior in \
                        language-tagged corpora")
        # Optional arguments
        parser.add_argument(
                "-l", "--langs",
                metavar=("lang1", "lang2"),
                nargs=2,
                default=[],
                required=True,
                help="languages in corpus")
        parser.add_argument(
                "-d", "--delimiter",
                help="delimiter for input file")
        parser.add_argument(
                "-v", "--verbose",
                action="store_true",
                help="verbose flag")
        parser.add_argument(
                "-c", "--column",
                metavar="n",
                help="zero-indexed language column in input file")
        parser.add_argument(
                "--header",
                action="store_true",
                help="header flag")

        # Positional arguments
        parser.add_argument(
                "infile",
                nargs="?",
                type=argparse.FileType("r"),
                default=sys.stdin,
                help="File containing corpus")
        parser.add_argument(
                "outfile",
                nargs="?",
                type=argparse.FileType("w"),
                default=sys.stdout,
                help="File containing metrics")

        args = parser.parse_args()

        if args.langs:
                LANGS = args.langs

        if args.delimiter:
                DELIMITER = args.delimiter

        if args.verbose:
                VERBOSE = True

        if args.column:
                LANGCOL = int(args.column)

        if args.header:
                HEADER = True

        if args.infile:
                INFILE = args.infile

        if args.outfile:
                OUTFILE = args.outfile

        main(sys.argv, len(sys.argv))
