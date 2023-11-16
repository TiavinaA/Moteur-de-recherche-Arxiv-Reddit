import pandas as pd
# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

#Méthode qui affiche toutes les infos d'un Document
    def __info__(self) :
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    
    def __str__(self) :
        return f"{self.titre}, par {self.auteur}"

class Author :
        # Initialisation des variables de la classe
    def __init__(self, name=""):
        self.name = name
        self.ndoc = 0
        self.production = []

    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    
class Corpus :
    def __init__(self, nom) :
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0 

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
    
    def showDocSortedByTitle(self, n_docs):
        docs = list(self.id2doc.values())
        docs = list(sorted(self.id2doc.values(), key=lambda x: x.titre.lower()))[:n_docs]
        for doc in docs:
            print(f"Document: {doc.titre} - Date: {doc.date}")
    
    def showDocSortedByDate(self, n_docs):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]
        for doc in docs:
            print(f"Document: {doc.titre} - Date: {doc.date}")

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        return "\n".join(list(map(str, docs)))  

    def save(self, file_path):
        # Crée un DataFrame à partir des données du corpus
        data = {
            'titre': [doc.titre for doc in self.id2doc.values()],
            'auteur': [doc.auteur for doc in self.id2doc.values()],
            'date': [doc.date for doc in self.id2doc.values()],
            'texte': [doc.texte for doc in self.id2doc.values()]
        }
        df = pd.DataFrame(data)

        # Enregistre le DataFrame au format CSV (ou tout autre format de votre choix)
        df.to_csv(file_path, index=False)  

    def load(self, file_path):
        # Charge le DataFrame depuis le fichier CSV
        df = pd.read_csv(file_path)

        # Ajoute les documents au corpus à partir du DataFrame
        for i, row in df.iterrows():
            doc = Document(row['titre'], row['auteur'], row['date'], row['texte'])
            self.add(doc)   
        
    