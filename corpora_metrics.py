#!/usr/bin/env python3
# metrics.py
# Using Python 3.4.3
#
# PURPOSE: Calculate various metrics to describe code-switching behavior in
# language-tagged corpora.

import sys
import math
import argparse
import numpy as np
from itertools import groupby
from collections import Counter

LANGS = []
LANGCOL = 0
NUMTAGS = 0
DELIMITER = "\t"
HEADER = False
VERBOSE = False
SWITCHPOINTS = False
INFILE = 0
OUTFILE = 0


def main(argc, argv):
        lang_tags = get_tags()
        num_switches = get_num_switchpoints(lang_tags)
        m_metric = get_m_metric(lang_tags)
        i_index = get_i_index(lang_tags)
        burstiness = get_burstiness(lang_tags)
        memory = get_memory(lang_tags)
        lang_entropy = get_lang_entropy(lang_tags)
        span_entropy = get_span_entropy(lang_tags)

        print("Length of corpus: {}".format(NUMTAGS))
        print("Number of switchpoints: {}".format(num_switches))
        print("M-metric: {}".format(m_metric))
        print("I-index: {}".format(i_index))
        print("Burstiness: {}".format(burstiness))
        print("Memory: {}".format(memory))
        print("Language Entropy: {}".format(lang_entropy))
        print("Span Entropy: {}".format(span_entropy))

        if SWITCHPOINTS:
                switchpoints = get_switchpoints(lang_tags)
                with open("Change_Vector.txt", mode="wt") as target:
                        target.write("\n".join(str(switch) for switch in
                                switchpoints))
                        target.write("\n")


def get_tags():
        global LANGS, NUMTAGS

        lang_tags = []

        # Read all language tags
        for line in INFILE:
                lang_tag = line.split(DELIMITER)[LANGCOL]
                lang_tags.append(lang_tag.strip())

        # Skip first line if header specified
        if HEADER:
                lang_tags = lang_tags[1:]

        # Assume input has no other tags
        if not LANGS:
                LANGS = list(set(lang_tags))
        # Otherwise, filter out non-language tags
        else:
                lang_tags = [lang for lang in lang_tags if lang in LANGS]

        NUMTAGS = len(lang_tags)

        # Print working set of language tags if needed
        if VERBOSE:
                print("Set of language tags: {}".format(LANGS))

        return lang_tags


def get_num_switchpoints(lang_tags):
        num_switches = 0

        for index, tag in enumerate(lang_tags[1:]):
                if tag != lang_tags[index - 1]:
                        num_switches += 1

        return num_switches


def get_m_metric(lang_tags):
        num_langs = len(LANGS)
        counts = Counter(lang_tags)


        # Compute p_i^2 for all languages in text
        p_lang = {}
        for lang, count in counts.items():
                p_lang[lang] = (count / float(NUMTAGS)) ** 2

        p_sum = sum(p_lang.values())
        m_metric = (1 - p_sum) / ((num_langs - 1) * p_sum)

        return m_metric


def get_i_index(lang_tags):
        # Count number of language switches for each language
        switches = {lang: {} for lang in LANGS}
        counts = Counter(zip(lang_tags, lang_tags[1:]))

        # Compute transition probabilities
        for (x, y), c in counts.items():
                switches[x][y] = c / float(NUMTAGS - 1)

        i_index = 0.0

        # Sum all probabilities of switching language
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


def get_spans(lang_tags):
        # List of span lengths
        return [len(list(group)) for lang, group in groupby(lang_tags)]


def get_switchpoints(lang_tags):
        switchpoints = []

        # Compute vector of switch indices
        for index, tag in enumerate(lang_tags[:-1]):
                if tag != lang_tags[index + 1]:
                        switchpoints.append(index + 1)
                else:
                        switchpoints.append(0)

        return switchpoints


def get_lang_entropy(lang_tags):
        # Count frequencies of language tokens
        counts = Counter(lang_tags)

        # Compute entropy based on unigram language tokens
        lang_entropy = 0.0
        for lang, count in counts.items():
                lang_prob = count / float(NUMTAGS)
                lang_entropy -= lang_prob * math.log2(lang_prob)

        return lang_entropy


def get_span_entropy(lang_tags):
        # Get frequencies of language spans
        span_lengths = get_spans(lang_tags)
        span_counts = Counter(span_lengths)
        total_count = len(span_lengths)

        # Compute entropy based on spans of language tokens
        span_entropy = 0.0
        for length, count in span_counts.items():
                span_prob = count / float(total_count)
                span_entropy -= span_prob * math.log2(span_prob)

        return span_entropy


if __name__ == "__main__":
        parser = argparse.ArgumentParser(
                description=("Calculate various metrics to describe "
                             "CS behavior in language-tagged corpora"))

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
                "--header",
                action="store_true",
                help="header flag  (Default: False)")
        parser.add_argument(
                "--switchpoints",
                action="store_true",
                help=("Compute vector of switchpoints "
                      "(Default: False)"))

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

        if args.switchpoints:
                SWITCHPOINTS = True

        DELIMITER = args.delimiter
        INFILE = args.infile
        LANGCOL = args.column
        LANGS = args.langs
        OUTFILE = args.outfile

        main(len(sys.argv), sys.argv)

        args.infile.close()
        args.outfile.close()
