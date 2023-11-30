from scipy.sparse import csr_matrix
from corpus import *
from corpusgenerator import * 
mots_sorted = sorted(list(corpus.vocabulaire))
# print(corpus.freq.sort_values(by='Mot'))
freq_mots = corpus.freq.sort_values(by='Mot')["Fréquence"]
vocab = {}
row_indices = []
col_indices = []
data = []
# Parcourir les mots et fréquences
for id_unique, (mot, frequence) in enumerate(zip(mots_sorted, freq_mots), start=1):
    vocab[mot] = {"id_unique": id_unique, "frequence": frequence}

for i, doc in enumerate(corpus.id2doc.values(), start=1):
    texte = nettoyer_texte(doc.texte)
    mots_doc = texte.split()
    # Compter les occurrences de chaque mot dans le document
    occurrences = {mot: mots_doc.count(mot) for mot in set(mots_doc)}

    for mot, occurrence in occurrences.items():
        if mot in corpus.vocabulaire:
            row_indices.append(i - 1)  # Les indices de ligne commencent à 0
            col_indices.append(mots_sorted.index(mot))
            data.append(occurrence)

shape = (len(corpus.id2doc), len(corpus.vocabulaire))
mat_TF = csr_matrix((data, (row_indices, col_indices)), shape=shape)
total_occurrences = mat_TF.sum(axis=0)  # Somme des colonnes pour obtenir les occurrences totales par mot
docs_contenant_mot = (mat_TF > 0).sum(axis=0)  # Somme des documents contenant chaque mot

# Mettre à jour le dictionnaire vocab avec les nouvelles informations
for mot, info in vocab.items():
    col_index = mots_sorted.index(mot)
    info["occurrences_totales"] = total_occurrences[0, col_index]
    info["docs_contenant_mot"] = docs_contenant_mot[0, col_index]

print(vocab)