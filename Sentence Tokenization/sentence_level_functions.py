"""
Python 3.6.0
2/7/2018

Test function file for sentence metrics
Functions to be tabulated take one input of a list of dicts representing each token. dict format is: {'lang': lang_val, 'POS': POS_val}. This argument is called `sent` under the assumption that the list represents a sentence, but it can represent any section of the data.
"""


import random as rm
from math import log2, sqrt


# settings
LANGS = {'eng', 'spa'}  # non-ignored languages (e.g. not punctuation)
REFLANG = 'eng'  # language to which calculations refer in reporting
IGNORE_LANG_SUBSET = {'NA'}  # subset of language tags to be ignored (e.g. punctuation)
POS_SUBSETS = {
    'FuncWord': {'ADP', 'CONJ', 'DET', 'PRON', 'FUNCV'},
    'Verb': {'FUNCV', 'CONTV'},
    'AuxVerb': {'FUNCV'}
}

N_LANGS = len(LANGS)

# for sharing info b/w functions
subset_size_this_sent = {subset_name: 0 for subset_name in POS_SUBSETS}


def SentLen(sent):
    '''number of countable tokens in the sentence'''
    count = 0
    for tok in sent:
        if tok['lang'] not in IGNORE_LANG_SUBSET:
            count += 1
    return count


def Frac_Reflang(sent):
    '''fraction of total words that are in the reference language'''
    n_reflang = 0
    n_sent = len(sent)
    for tok in sent:
        if tok['lang'] == REFLANG:
            n_reflang += 1
        elif tok['lang'] in IGNORE_LANG_SUBSET:
            n_sent -= 1
    if n_sent > 0:
        return n_reflang / n_sent
    return 'undef'


def I_Index(sent):
    '''number of language switches per switchpoint'''

    # set up
    switches = 0
    switchpoints = len(sent) - 1

    # find first countable token (usually right at start)
    try:
        i = 0
        lastlang = sent[0]['lang']
        while lastlang in IGNORE_LANG_SUBSET:
            i += 1
            lastlang = sent[i]['lang']
    except IndexError:
        return 'undef'

    # compute
    for tok in sent[i + 1:]:
        thislang = tok['lang']
        if thislang in IGNORE_LANG_SUBSET:
            switchpoints -= 1
        else:
            if thislang != lastlang:
                switches += 1
                lastlang = thislang
    if switchpoints > 0:
        return switches / switchpoints
    return 'undef'


def M_Index(sent):
    '''the Multilingual Index as defined by Barnett et al. (1999)'''
    n = {}
    N = 0
    for tok in sent:
        if tok['lang'] not in IGNORE_LANG_SUBSET:
            if tok['lang'] in n:
                n[tok['lang']] += 1
            else:
                n[tok['lang']] = 1
            N += 1
    p = {lang: n[lang] / N for lang in n}
    sum_pj2 = sum(map(lambda x: x ** 2, p.values()))
    if sum_pj2 > 0:
        return (1 - sum_pj2) / (N_LANGS - 1) / sum_pj2
    return 'undef'


def POSSubsetReflangFrac(subset_name):
    def func(sent):
        '''fraction of words in the POS subset that are in the reference language'''
        n_subset = n_reflang = 0
        for tok in sent:
            if tok['POS'] in POS_SUBSETS[subset_name]:
                n_subset += 1
                if tok['lang'] == REFLANG:
                    n_reflang += 1
        subset_size_this_sent[subset_name] = n_subset
        if n_subset > 0:
            return n_reflang / n_subset
        return 'undef'

    func.__name__ = subset_name + 'ReflangFrac'
    return func


def SampleReflangFrac(sent, size):
    '''creates a control group the same size as a particular POS subset'''
    if size > 0:
        n_reflang = 0
        for tok in rm.sample(sent, size):
            if tok['lang'] == REFLANG:
                n_reflang += 1
        return n_reflang / size
    return 'undef'


for subset_name in POS_SUBSETS:
    exec('{0}ReflangFrac = POSSubsetReflangFrac("{0}")'.format(subset_name))
    exec('''\
def Compare{0}Frac(sent):
    return SampleReflangFrac(sent, subset_size_this_sent['{0}'])\
'''.format(subset_name))


def LanguageEntropy(sent):
    '''shannon entropy of the language frequencies'''
    freqs = {}
    for tok in sent:
        if tok['lang'] in LANGS:
            if tok['lang'] in freqs:
                freqs[tok['lang']] += 1
            else:
                freqs[tok['lang']] = 1
    tot = sum(freqs.values())
    for lang in freqs:
        freqs[lang] /= tot
    return -sum(map(lambda freq: freq * log2(freq), freqs.values()))


def spanlen(x):
    '''to access the length of a span'''
    return x[1]


def get_span_info(sent):  # use in first function that requires it so only needs to be called once per sentence
    '''set global span-related variables'''
    global spans, spansum, nr, nr_1
    spans = []
    for tok in sent:
        if len(spans) > 0 and spans[-1][0] == tok['lang']:
            spans[-1][1] += 1
        elif tok['lang'] in LANGS:
            spans.append([tok['lang'], 1])
    spansum = sum(map(spanlen, spans))
    nr = len(spans)
    nr_1 = nr - 1


def Memory(sent):
    '''as defined by Goh & Barabási, 2008, applied to span lengths'''
    get_span_info(sent)
    if nr_1 < 1:
        return 'undef'
    m1 = (spansum - spans[-1][1]) / nr_1  # mean of all span lengths except last
    m2 = (spansum - spans[0][1]) / nr_1  # mean of all span lengths except first
    sumsq1 = sumsq2 = 0  # sums of squares of residuals
    memsum = 0  # the summation in the memory equation, excluding the standard deviations (calculated simultaneously)
    spanlens = map(spanlen, spans)
    lastresid = next(spanlens) - m1
    for i in range(nr_1 - 1):
        thislen = next(spanlens)
        thisresid = thislen - m2
        sumsq1 += lastresid ** 2
        sumsq2 += thisresid ** 2
        memsum += lastresid * thisresid
        lastresid = thislen - m1
    thisresid = next(spanlens) - m2
    sumsq1 += lastresid ** 2
    sumsq2 += thisresid ** 2
    sumsqprod = sumsq1 * sumsq2
    if not sumsqprod:
        return 'undef'
    memsum += lastresid * thisresid
    return memsum / sqrt(sumsqprod)


def SpanEntropyByCondition(condition=lambda spanlang: True):
    def func(sent):
        '''Shannon entropy of span distribution, restricted by a condition function on languages'''
        if len(spans) > 0:
            freqs = {}
            for spanlang, L in spans:
                if condition(spanlang):
                    if L in freqs:
                        freqs[L] += 1
                    else:
                        freqs[L] = 1
            tot = sum(freqs.values())
            for L in freqs:
                freqs[L] /= tot  # now relative frequencies, i.e. p
            return -sum(map(lambda p: p * log2(p), freqs.values()))
        return 'undef'

    func.__name__ = 'SpanEntropy'
    return func


SpanEntropy = SpanEntropyByCondition()


def SpanEntropyByLang(lang):
    '''span entropy of a single language'''
    func = SpanEntropyByCondition(lambda spanlang: spanlang == lang)
    func.__name__ = lang[0].upper() + lang[1:].lower() + 'SpanEntropy'
    return func


EngSpanEntropy = SpanEntropyByLang('eng')
SpaSpanEntropy = SpanEntropyByLang('spa')


def Burstiness(sent):
    if nr < 1:
        return 'undef'
    m = spansum / nr
    sumsq = 0  # sum of squared residuals
    for L in map(spanlen, spans):
        sumsq += (L - m) ** 2
    sigma = sqrt(sumsq / nr)
    return (sigma - m) / (sigma + m)


# required for sentence metrics script
FUNCTIONS = [Frac_Reflang, I_Index, M_Index, FuncWordReflangFrac, VerbReflangFrac, AuxVerbReflangFrac, CompareFuncWordFrac, CompareVerbFrac, CompareAuxVerbFrac, LanguageEntropy, Memory, Burstiness, SpanEntropy, EngSpanEntropy, SpaSpanEntropy]
