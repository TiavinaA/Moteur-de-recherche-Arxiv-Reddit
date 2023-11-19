from csvgenerator import *
corpus_charge = Corpus('CorpusTest')
corpus_charge.load('corpus.csv')
print(repr(corpus_charge))
