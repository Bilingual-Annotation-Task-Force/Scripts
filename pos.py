import torch
from flair.data import Sentence

from flair.models import SequenceTagger
tagger = SequenceTagger.load("pos-multi")

with open("real_feature.txt") as f:
    for l in f:
        sentence = Sentence(l)
        tagger.predict(sentence)
        print(sentence.to_tagged_string(), file=open("KC_pos.txt", "a"))
