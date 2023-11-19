from author import *
from document import *
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
            'url' : [doc.url for doc in self.id2doc.values()],
            'texte': [doc.texte for doc in self.id2doc.values()],
            'type' : [doc.type for doc in self.id2doc.values()],
            'nbCom': [doc.nbCom if hasattr(doc, 'nbCom') else None for doc in self.id2doc.values()]
        }
        df = pd.DataFrame(data)

        # Enregistre le DataFrame au format CSV (ou tout autre format de votre choix)
        df.to_csv(file_path, index=False)  

    def load(self, file_path):
        # Charge le DataFrame depuis le fichier CSV
        df = pd.read_csv(file_path)

        # Ajoute les documents au corpus à partir du DataFrame
        for i, row in df.iterrows():
            if row['type'] == 'Reddit':
                doc = RedditDocument(row['titre'], row['auteur'], row['date'], row['url'],row['texte'])
                doc.nbCom = row['nbCom']
            elif row['type'] == 'Arxiv':
                doc = ArxivDocument(row['titre'], row['auteur'], row['date'], row['url'],row['texte'])

            self.add(doc)

 
        