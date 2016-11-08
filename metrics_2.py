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

        # Assume input has no other tags
        if not LANGS:
                LANGS = list(set(lang_tags))
        # Otherwise, filter out non-language tags
        else:
                lang_tags = [lang for lang in lang_tags if lang in LANGS]

        return lang_tags


def main(argc, argv):
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

        # Compute p_i^2 for all languages in text
        p_lang = {}
        for lang in LANGS:
                p_lang[lang] = len([x for x in lang_tags if x == lang])
                p_lang[lang] = (p_lang[lang] / float(total)) ** 2

        p_sum = sum(p_lang.values())
        m_metric = (1 - p_sum) / ((k - 1) * p_sum)

        return m_metric


def get_i_index(lang_tags):
        switches = {lang: {} for lang in set(lang_tags)}
        counts = Counter(zip(lang_tags, lang_tags[1:]))

        total = len(lang_tags) - 1

        # Compute transition probabilites
        for (x, y), c in counts.items():
                switches[x][y] = c / float(total)

        i_index = 0.0

        # Sum all probabilities where there is a language switch
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
                memory += (span - mean1) * (spans[i + 1] - mean2)

        memory /= (len(spans) - 1) * (sd1 * sd2)

        return memory


def get_spans(lang_tags):  # Include last span?
        return [len(list(group)) for lang, group in groupby(lang_tags)]


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
                help="languages in corpus")
        parser.add_argument(
                "-d", "--delimiter",
                nargs="?",
                type=str,
                default="\t",
                help="delimiter for input file")
        parser.add_argument(
                "-v", "--verbose",
                action="store_true",
                help="verbose flag")
        parser.add_argument(
                "-c", "--column",
                metavar="n",
                nargs="?",
                type=int,
                default=0,
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

        if args.verbose:
                VERBOSE = True

        if args.header:
                HEADER = True

        DELIMITER = args.delimiter
        INFILE = args.infile
        LANGCOL = args.column
        LANGS = args.langs
        OUTFILE = args.outfile

        main(len(sys.argv), sys.argv)
