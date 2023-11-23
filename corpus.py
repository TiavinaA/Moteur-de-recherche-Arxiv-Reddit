from author import *
from document import *
import pickle
from singleton_decorator import singleton

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
        # Serialize the entire corpus object using pickle
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    def load(self, file_path):
        # Deserialize the corpus object from the pickle file
        with open(file_path, 'rb') as file:
            loaded_corpus = pickle.load(file)
            return loaded_corpus
    

            

 
        