from flair.data import TaggedCorpus, Sentence
from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings
from typing import List
from flair.models import SequenceTagger
from torch.optim.adam import Adam

columns = {0: 'text', 1: 'pos'}
data_folder = 'data/'
corpus: TaggedCorpus = NLPTaskDataFetcher.load_column_corpus(data_folder, columns,
                                                              train_file='Miami_Universal_Tagged.tsv',
                                                              test_file='S7_Universal_Tagged.tsv',
                                                              dev_file='KC_ARIS_Universal_Tagged.tsv')
temp = corpus.train[0]
def split_sentence(tokens, seq_len = 30):
  tokens = [tokens[i: seq_len+i] for i in range(0, len(tokens), seq_len)]
  train = []
  for t in tokens:
    s = Sentence()
    s.tokens = t
    train.append(s)
  return train
train = split_sentence(corpus.train[0])
print(corpus.test)
test = split_sentence(corpus.test[0])
dev = split_sentence(corpus.dev[0])
print(len(train))
print(len(test))
print(len(dev))
corpus = TaggedCorpus(train, dev, test)
tag_type = 'pos'
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary.idx2item)
embedding_types: List[TokenEmbeddings] = [
    FlairEmbeddings('news-forward'),
    FlairEmbeddings('news-backward'),
    FlairEmbeddings('spanish-forward'),
    FlairEmbeddings('spanish-backward')
]
embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
tagger: SequenceTagger = SequenceTagger(
    hidden_size=512,
    embeddings=embeddings,
    tag_dictionary=tag_dictionary,
    tag_type=tag_type,
    use_rnn=True,
    use_crf=True,
    rnn_layers = 3,
    dropout = 0.3
)


from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus, optimizer = Adam)
trainer.train('resources/taggers/pos',
              learning_rate = 1e-4,
              mini_batch_size=32,
              max_epochs=50)


