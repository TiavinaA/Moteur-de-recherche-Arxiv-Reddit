import pandas as pd
#Chargement du corpus en mémooire sans interroger l'api
corpus = pd.read_csv('corpusTD3.csv', sep='\t')
#Affichage de la taille du corpus
print("Longueur du corpus : " + str(len(corpus)))
# Itération sur les lignes du DataFrame
for index, row in corpus.iterrows():
    # Nombre de phrases
    print("Nombre de phrases pour le document {}: {}".format(index, len(row['texte'].split("."))))
    # Nombre de mots
    print("Nombre de mots pour le document {}: {}".format(index, len(row['texte'].split(" "))))
