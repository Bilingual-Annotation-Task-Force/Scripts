#!/usr/bin/env python3
# compile.py

import os

# directory = "/Users/jacqueline/Dropbox/spoken/face-to-face"
directory = "/Users/jacqueline/Dropbox/Data/activ-es-master/activ-es-v.01/corpus/plain/"

if __name__ == "__main__":
    os.chdir(directory)
    corpus = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".run") or not file.startswith("es_M"):
                continue
            print(root, file)
            with open(root + "/" + file) as fp:
                text = fp.read()
            corpus.append(text)

    with open("/Users/jacqueline/Desktop/MexCorpus.txt", "w") as output:
        output.write("".join(corpus))
    print(*corpus, sep="\n")
