from csvgenerator import *
from corpus import *
corpus.construire_vocabulaire()
corpus.construire_freq()

corpus.stats(10)