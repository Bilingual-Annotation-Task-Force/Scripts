"""
Eric Nordstrom
Python 3.6.0
2/7/2018

Test function file for sentence metrics
Functions to be tabulated take one input of a list of dicts for each token. dict format is: {'lang': lang_val, 'POS': POS_val}. This argument will be called `sent` assuming the list represents a sentence.
"""


# to change depending on data
reflang = 'ENG'  # language to which calculations refer in reporting
punc_lang_tagset = {'PUNC'}  # subset of language tags indicating the token is punctuation
function_words_tagset = {'FUNC'}  # subset of POS tags that are considered function words


def Frac_Reflang(sent):
    n_reflang = 0
    n_sent = len(sent)
    for tok in sent:
        if tok['lang'] == reflang:
            n_reflang += 1
        elif tok['lang'] in punc_lang_tagset:
            n_sent -= 1
    return n_reflang / n_sent


def I_Metric(sent):
    '''number of language switches per switchpoint'''

    # setup
    switches = 0
    switchpoints = len(sent) - 1

    # find first countable token (usually right at start)
    i = 0
    lastlang = sent[0]['lang']
    while lastlang in punc_lang_tagset:
        i += 1
        lastlang = sent[i]['lang']

    # compute
    for tok in sent[i + 1:]:
        thislang = tok['lang']
        if thislang in punc_lang_tagset:
            switchpoints -= 1
        else:
            if thislang != lastlang:
                switches += 1
                lastlang = thislang

    return switches / switchpoints


def FuncWordReflangFrac(sent):
    '''fraction of function words that are in the reference language'''
    n_funcwords = n_reflang = 0
    for tok in sent:
        if tok['POS'] in function_words_tagset:
            n_funcwords += 1
            if tok['lang'] == reflang:
                n_reflang += 1
    return n_reflang / n_funcwords
