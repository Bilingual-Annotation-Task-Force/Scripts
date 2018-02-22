"""
Python 3.6.0
2/7/2018

Test function file for sentence metrics
Functions to be tabulated take one input of a list of dicts representing each token. dict format is: {'lang': lang_val, 'POS': POS_val}. This argument is called `sent` under the assumption that the list represents a sentence, but it can represent any section of the data.
"""


# settings
REFLANG = 'ENG'  # language to which calculations refer in reporting
PUNC_LANG_SUBSET = {'PUNC'}  # subset of language tags indicating the token is punctuation
FUNCWORD_POS_SUBSET = {'FUNC', 'VFUNC'}  # subset of POS tags that are considered function words
VERB_POS_SUBSET = {'VFUNC', 'VCONT'}  # subset of POS tags that are considered verbs
N_LANGS = 2  # number of languages present


def Frac_Reflang(sent):
    '''fraction of total words that are in the reference language'''
    n_reflang = 0
    n_sent = len(sent)
    for tok in sent:
        if tok['lang'] == REFLANG:
            n_reflang += 1
        elif tok['lang'] in PUNC_LANG_SUBSET:
            n_sent -= 1
    return n_reflang / n_sent


def I_Index(sent):
    '''number of language switches per switchpoint'''

    # setup
    switches = 0
    switchpoints = len(sent) - 1

    # find first countable token (usually right at start)
    i = 0
    lastlang = sent[0]['lang']
    while lastlang in PUNC_LANG_SUBSET:
        i += 1
        lastlang = sent[i]['lang']

    # compute
    for tok in sent[i + 1:]:
        thislang = tok['lang']
        if thislang in PUNC_LANG_SUBSET:
            switchpoints -= 1
        else:
            if thislang != lastlang:
                switches += 1
                lastlang = thislang

    return switches / switchpoints


def _POSSubsetReflangFrac(POS_subset):
    def func(sent):
        '''fraction of words in the POS subset that are in the reference language'''
        n_subset = n_reflang = 0
        for tok in sent:
            if tok['POS'] in POS_subset:
                n_subset += 1
                if tok['lang'] == REFLANG:
                    n_reflang += 1
        return n_reflang / n_subset
    return func

FuncWordReflangFrac = _POSSubsetReflangFrac(FUNCWORD_POS_SUBSET)
VerbReflangFrac = _POSSubsetReflangFrac(VERB_POS_SUBSET)


def M_Index(sent):
    '''the Multilingual Index as defined by Barnett et al. (1999)'''
    n = {}
    N = 0
    for tok in sent:
        if tok['lang'] not in PUNC_LANG_SUBSET:
            if tok['lang'] in n:
                n[tok['lang']] += 1
            else:
                n[tok['lang']] = 1
            N += 1
    p = {lang: n[lang] / N for lang in n}
    sum_pj2 = sum(map(lambda x: x ** 2, p.values()))
    return (1 - sum_pj2) / (N_LANGS - 1) / sum_pj2
