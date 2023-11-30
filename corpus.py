from author import *
from document import *
import pickle
import re


class Corpus :
    def __init__(self, nom) :
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0 
        self.chaineunique = None
        self.vocabulaire = set()
        self.freq = None

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        # Mettez à jour la chaîne unique après chaque ajout de document
        self.mettre_a_jour_chaineunique()

    def construire_chaineunique(self):
        return " ".join(doc.texte for doc in self.id2doc.values())

    def mettre_a_jour_chaineunique(self):
        self.chaineunique = self.construire_chaineunique()

    def construire_vocabulaire(self) :
        for doc in self.id2doc.values() :
            texte = nettoyer_texte(doc.texte)
            mots = texte.split()  # Utilisation de split sans expression régulière
            self.vocabulaire.update(mots)
    
    def construire_freq(self):
        # Initialiser un dictionnaire avec des zéros pour chaque mot du vocabulaire
        freq_dict = {mot: 0 for mot in self.vocabulaire}

        for doc in self.id2doc.values():
            texte = nettoyer_texte(doc.texte)
            mots = texte.split()

            # Mettre à jour le dictionnaire de fréquences
            for mot in mots:
                if mot in freq_dict:
                    freq_dict[mot] += 1

        # Construire un tableau pandas à partir du dictionnaire de fréquences
        self.freq = pd.DataFrame(list(freq_dict.items()), columns=['Mot', 'Fréquence'])

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
            
    def search(self, keyword):
        results = {}
        pattern = re.compile(r'\b{}\b'.format(re.escape(keyword)), re.IGNORECASE)

        longueChaineDeCaracteres = " ".join(doc.texte for doc in self.id2doc.values())

        matches = pattern.finditer(self.chaineunique)
        for match in matches:
            start, end = match.span()
            passage = self.chaineunique[max(0, start - 20):min(len(self.chaineunique), end + 20)]

            results.setdefault(match.group(), []).append((start, end, passage))

        return results
    
    def concordance(self, expression, contexte_size):
        if self.chaineunique is None:
            self.mettre_a_jour_chaineunique()

        results = {
            "Contexte Gauche": [],
            "Motif Trouvé": [],
            "Contexte Droit": []
        }

        pattern = re.compile(r'\b{}\b'.format(re.escape(expression)), re.IGNORECASE)

        matches = pattern.finditer(self.chaineunique)
        for match in matches:
            start, end = match.span()
            debut_contexte = max(0, start - contexte_size)
            fin_contexte = min(len(self.chaineunique), end + contexte_size)

            contexte_gauche = self.chaineunique[debut_contexte:start]
            motif_trouve = self.chaineunique[start:end]
            contexte_droit = self.chaineunique[end:fin_contexte]

            results["Contexte Gauche"].append(contexte_gauche)
            results["Motif Trouvé"].append(motif_trouve)
            results["Contexte Droit"].append(contexte_droit)

        # Créer un DataFrame pandas pour stocker les résultats
        concordance_df = pd.DataFrame(results)
        return concordance_df
    

    def stats(self, n) :
        n_mots = len(self.vocabulaire)
        f = self.freq.sort_values(by='Fréquence', ascending=False)
        top_mots = f.head(n)
        print(f"Nombre de mots différents dans le Corpus : {n_mots}\n"
          f"Les {n} mots les plus fréquents :\n {top_mots.to_string(index=False)}")
    

def nettoyer_texte(texte):
    # Mise en minuscules
    texte = texte.lower()
    # Remplacement des retours à la ligne
    texte = texte.replace('\n', ' ')
    # Suppression des ponctuations et des chiffres
    texte = re.sub(r'[^a-z ]', '', texte)

    return texte

        





 
        