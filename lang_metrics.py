#!/usr/bin/env python3
# lang_metrics.py
# Using Python 3.4.3
"""PURPOSE: Calculate various metrics to describe code-switching behavior in language-tagged corpora."""

import sys
import math
import argparse
import numpy as np
from itertools import groupby
from collections import Counter

LANGS = []
LANG_TAGS = []
LANGCOL = 0
NUMTAGS = 0
DELIMITER = "\t"
HEADER = False
VERBOSE = False
INFILE = 0
OUTFILE = 0


def main(func):
        global LANGS, NUMTAGS, LANG_TAGS

        for line in INFILE:
                lang_tag = line.split(DELIMITER)[LANGCOL]
                LANG_TAGS.append(lang_tag.strip())

        # Skip first line if header specified
        if HEADER:
                LANG_TAGS = LANG_TAGS[1:]

        # Assume input has no other tags
        if not LANGS:
                LANGS = list(set(LANG_TAGS))
        # Otherwise, filter out non-language tags
        else:
                LANG_TAGS = [lang for lang in LANG_TAGS if lang in LANGS]

        NUMTAGS = len(LANG_TAGS)

        # Print working set of language tags if needed
        if VERBOSE:
                print("Set of language tags: {}".format(LANGS))
                print("Length of corpus: {}".format(NUMTAGS))

        func_map = {
                'metrics': metrics,
                'm_metric': m_metric,
                'i_metric': i_metric,
                'burstiness': burstiness,
                'memory': memory,
                'spans': spans,
                'span_summary': span_summary,
                'switchpoints': switchpoints,
                'lang_entropy': lang_entropy,
                'span_entropy': span_entropy,
                }

        func_map[func]()


def metrics():
        num_switchpoints()
        m_metric()
        i_metric()
        burstiness()
        memory()
        lang_entropy()
        span_entropy()


def num_switchpoints():
        num_switches = 0

        for index, tag in enumerate(LANG_TAGS[1:]):
                if tag != LANG_TAGS[index - 1]:
                        num_switches += 1

        print("Number of switchpoints: {}".format(num_switches))


def m_metric():
        num_langs = len(LANGS)
        counts = Counter(LANG_TAGS)


        # Compute p_i^2 for all languages in text
        p_lang = {}
        for lang, count in counts.items():
                p_lang[lang] = (count / float(NUMTAGS)) ** 2

        p_sum = sum(p_lang.values())
        m_metric = (1 - p_sum) / ((num_langs - 1) * p_sum)

        print("M-metric: {}".format(m_metric))


def i_metric():
        # Count number of language switches for each language
        switches = {lang: {} for lang in LANGS}
        counts = Counter(zip(LANG_TAGS, LANG_TAGS[1:]))

        # Compute transition probabilities
        for (x, y), c in counts.items():
                switches[x][y] = c / float(NUMTAGS - 1)

        i_metric = 0.0

        # Sum all probabilities of switching language
        for lang1, switch in switches.items():
                for lang2, prob in switch.items():
                        if lang1 != lang2:
                                i_metric += prob

        print("I-metric: {}".format(i_metric))


def burstiness():
        spans = [len(list(group)) for lang, group in groupby(LANG_TAGS)]
        mean = np.mean(spans)
        sd = np.std(spans)
        burstiness = (sd - mean)/(sd + mean)

        print("Burstiness: {}".format(burstiness))


def memory():
        spans = [len(list(group)) for lang, group in groupby(LANG_TAGS)]
        mean1 = np.mean(spans[:-1])
        mean2 = np.mean(spans[1:])
        sd1 = np.std(spans[:-1])
        sd2 = np.std(spans[1:])
        memory = 0.0

        for i, span in enumerate(spans[:-1]):
                memory += (span - mean1) * (spans[i + 1] - mean2)

        memory /= (len(spans) - 1) * (sd1 * sd2)

        print("Memory: {}".format(memory))


def spans():
        spans = [(lang, len(list(group))) for lang, group in groupby(LANG_TAGS)]

        print("Lang\tLength")

        for lang, length in spans:
                print("{}\t{}".format(lang, length))


def span_summary():
        spans = sorted([(lang, len(list(group))) for lang, group in groupby(LANG_TAGS)])
        spans = sorted([(c, len(list(cgen))) for c, cgen in groupby(spans)])

        print("Lang\tSpanLength\tSpanFreq")

        for (lang, length), freq in spans:
                print("{}\t{}\t{}".format(lang, length, freq))


def switchpoints():
        switchpoints = []

        # Compute vector of switch indices
        for index, tag in enumerate(LANG_TAGS[:-1]):
                if tag != LANG_TAGS[index + 1]:
                        switchpoints.append(index + 1)
                else:
                        switchpoints.append(0)

        for switch in switchpoints:
                print("{}".format(switch))


def lang_entropy():
        # Count frequencies of language tokens
        counts = Counter(LANG_TAGS)

        # Compute entropy based on unigram language tokens
        lang_entropy = 0.0
        for lang, count in counts.items():
                lang_prob = count / float(NUMTAGS)
                lang_entropy -= lang_prob * math.log2(lang_prob)

        print("Language Entropy: {}".format(lang_entropy))


def span_entropy():
        # Get frequencies of language spans
        spans = [len(list(group)) for lang, group in groupby(LANG_TAGS)]
        span_counts = Counter(spans)
        total_count = len(spans)

        # Compute entropy based on spans of language tokens
        span_entropy = 0.0
        for length, count in span_counts.items():
                span_prob = count / float(total_count)
                span_entropy -= span_prob * math.log2(span_prob)

        print("Span Entropy: {}".format(span_entropy))


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
                "-f", "--function",
                type=str,
                default="metrics",
                help=("Possible functions: "
                      "metrics, m_metric, i_metric, burstiness, memory, "
                      "spans, span_summary, switchpoints, lang_entropy, "
                      "span_entropy. (Default: metrics)"))

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
        LANGCOL = args.column
        LANGS = args.langs
        OUTFILE = args.outfile

        main(args.function)

        args.infile.close()
        args.outfile.close()
