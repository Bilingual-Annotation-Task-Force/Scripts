import unittest
from sentence_level_functions import *
import logging
logging.basicConfig(level=logging.WARNING)

# settings
REFLANG = 'ENG'
PUNC_LANG_SUBSET = {'PUNC'}
FUNCWORD_POS_SUBSET = {'FUNC', 'VFUNC'}
VERB_POS_SUBSET = {'VFUNC', 'VCONT'}
N_LANGS = 2

# inputs
sents = [[]]
with open('sentence metrics test.tsv') as f:
    next(f)  # skip header
    for line in f:
        tok = line.rstrip().split('\t')
        logging.debug('token: {}'.format(tok))
        sents[-1].append({'lang': tok[1], 'POS': tok[2]})
        if tok[0] == '.':
            sents.append([])
info_msg = ''
for sent in sents:
    for tok in sent:
        info_msg += '\t{}\n'.format(tok)
    info_msg += '\n'
logging.info('Sentences:\n' + info_msg)

"""
                Sentence 1      Sentence 2      Sentence 3
                tot ENG SPN     tot ENG SPN     tot ENG SPN
Words:          4   4   0       9   4   5       5   0   5
Func. words:    3   3   0       5   3   2       3   0   3
Verbs:          1   1   0       3   1   2       3   0   3
Switches:           0               2               0
"""

# expected outputs
answers = {
    'Frac_Reflang': [1, 4 / 9, 0],
    'I_Index': [0, 0.25, 0],
    'FuncWordReflangFrac': [1, 0.6, 0],
    'VerbReflangFrac': [1, 1 / 3, 0],
    'M_Index': [0, (1 - (4 / 9) ** 2 - (5 / 9) ** 2) / ((4 / 9) ** 2 + (5 / 9) ** 2), 0]
}


class TestSentenceLevelFunctions(unittest.TestCase):
    test_code_template = '''\
def test_{0}(self):
    for sent, answer in zip(sents, answers['{0}']):
        self.assertEqual({0}(sent), answer)\
'''

    for funcname in answers:
        exec(test_code_template.format(funcname))

if __name__ == '__main__':
    unittest.main()
