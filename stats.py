#!/usr/bin/env python3
# stats.py
# Using Python 3.5.2

import io
import sys
from typing import Dict, List

# region Tags

L0_TAG = "Eng"
L1_TAG = "Spn"
NE_TAG = "NamedEnt"

TAG_LIST = [L0_TAG, L1_TAG, NE_TAG]
LANG_TAGS = [L0_TAG, L1_TAG]
SPECIAL_TAGS = [NE_TAG]
GOLD_MATCH = {L0_TAG: "Eng", L1_TAG: "Spn", NE_TAG: "NamedEnt"}
PROCESSED_MATCH = {L0_TAG: "Eng", L1_TAG: "Spn", NE_TAG: "NamedEnt"}

# endregion

# region Stats

TP = "tp"
FN = "fn"
FP = "fp"
TN = "tn"
PRELIM_STATS = [TP, FN, FP, TN]

ACCURACY = "Accuracy"
PRECISION = "Precision"
RECALL = "Recall"
STATS_LIST = [ACCURACY, PRECISION, RECALL]

# region Formulae


def accuracy_calc(tp, fn, fp, tn, **kwargs):
    """Accuracy = (TP + TN)/(TP + TN + FP + FN)"""
    pre = tp + tn
    return pre / float(fp + fn + pre)


def precision_calc(tp, fp, **kwargs):
    """Precision = TP/(TP + FP)"""
    return tp / float(tp + fp)


def recall_calc(tp, fn, **kwargs):
    """Recall = TP / (TP + FN)"""
    return tp / float(tp + fn)


# endregion

STATS_FUNC_DICT = {
    ACCURACY: accuracy_calc,
    PRECISION: precision_calc,
    RECALL: recall_calc
}


# endregion


def calc_stats(counts: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    """Calculate all stats in the dictionary STATS_FUNC for tags in TAG_LIST and stats in STATS_LIST.

    :param counts: Double layered dictionary of tags to preliminary stats to values
    :return: Values of the calculated stats
    """
    calc = {}
    for tag in TAG_LIST:
        calc[tag] = {}
        print(tag, ":", sep="", end="")
        for stat in STATS_LIST:
            calc[tag][stat] = STATS_FUNC_DICT[stat](**counts[tag])
            print(stat, " ", calc[tag][stat], ",", sep="", end="")
    return calc


def count(tag, orig_tag, check_tag, counts):
    # Count the respective values
    if orig_tag == GOLD_MATCH[tag]:
        if check_tag == PROCESSED_MATCH[tag]:
            counts[tag][TP] += 1
        else:
            counts[tag][FN] += 1
    else:
        if check_tag == tag:
            counts[tag][FP] += 1
        else:
            counts[tag][TN] += 1


def main(argv: List[str]) -> None:
    """Takes processed data and converts it into a set of statistics for the processing program.

    :param argv: Either the file in question, or the source file.
    """
    lines = []
    if len(sys.argv) == 1:
        with open(argv[0], "r", encoding="utf8") as file:
            lines = file.readlines()
        lines = map(lambda padded_line: padded_line.strip(), lines)
    else:
        for line in sys.stdin:
            lines.append(line.strip())
    lines = [x.split() for x in lines]
    lines = [x for x in lines if x[0] in TAG_LIST]

    # Transpose tag listings
    (gold_list, processed_list, special_list) = map(list, zip(*lines))
    special_list = list(map(lambda d: "Something not the tag" if d == "O" else "NamedEnt", special_list))

    # Make a dictionary of dictionaries of preliminary stats
    counts = {tag: {TP: 0, FN: 0, FP: 0, TN: 0} for tag in TAG_LIST}

    # For every pair of gold standard and processed tags
    for (gold_tag, processed_tag, special_tag) in zip(gold_list, processed_list, special_list):
        # For each tag
        for tag in LANG_TAGS:
            count(tag, gold_tag, processed_tag, counts)
        for tag in SPECIAL_TAGS:
            count(tag, gold_tag, special_tag, counts)
    print(counts)

    calc_stats(counts)


if __name__ == "__main__":
    main(sys.argv[1:])
