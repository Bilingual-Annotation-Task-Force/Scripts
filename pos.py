import torch
from flair.data import Sentence
from flair.models import SequenceTagger
import pickle

"""
Uses flair's multi lingual tagger to tag given document.

The input file should be white space tokenized with a \n seperating
each sentence.
    For example:
        The keys, which were needed to access the building, were locked in the car.\n
    should become:
        The keys , which were needed to access the building , were locked in the car .\n

Outputs a human readable version at POS_OUT_FILE,
as well as a serialized version at PICKLE_FILE
"""
INPUT_FILE = "real_feature.txt"
POS_OUT_FILE = "KC_pos.txt"
PICKLE_FILE = "KC_pos_pickle"
ENCODING = "utf-8-sig"
if __name__ == "__main__":
    tagger = SequenceTagger.load("pos-multi")
    with open(INPUT_FILE, encoding = ENCODING) as f:
        sentences = []
        # empty the contents
        with open(POS_OUT_FILE, "w") as p, open(PICKLE_FILE, "w") as pp:
            pass
        with open(POS_OUT_FILE, "a", encoding = ENCODING) as p:
            for l in f:
                # construct and parse the sentence
                sentence = Sentence(l)
                tagger.predict(sentence)
                # append sentence to a list for pickle
                sentences.append(sentence)
                # print readable version to the file
                print(sentence.to_tagged_string(), file=p)
            print("done outputing readable POS tag")
        # pickles a list of Sentence object to file for quick access
        with open(PICKLE_FILE, "wb") as pp:
            pickle.dump(sentences, pp)
            print("done outputing serialized object")