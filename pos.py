import torch
from flair.data import Sentence
from flair.models import SequenceTagger
import pickle


if __name__ == "__main__":
    tagger = SequenceTagger.load("pos-multi")
    with open("real_feature.txt", encoding = "utf-8-sig") as f:
        sentences = []
        # empty the contents
        with open("KC_pos.txt", "w") as p, open("KC_pos_pickle", "w") as pp:
            pass
        with open("KC_pos.txt", "a", encoding = "utf-8-sig") as p:
            for l in f:
                sentence = Sentence(l)
                tagger.predict(sentence)
                sentences.append(sentence)
                print(sentence.to_tagged_string(), file=p)
            print("done outputing readable POS tag")
        with open("KC_pos_pickle", "wb") as pp:
            pickle.dump(sentences, pp)
            print("done outputing serialized object")