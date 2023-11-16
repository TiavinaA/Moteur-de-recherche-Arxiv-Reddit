import praw
import urllib
import xmltodict
import pandas as pd
from classes import *
import datetime

docs = []

#Cette variable contient les documents en bruts pris sur Reddit et Arxiv
docs_bruts = []

#Récupération des documents de Reddit
reddit = praw.Reddit(client_id='nzJcQWMzVE8P6uYYll0-Bg', client_secret='s3M97y4jzMOiNr1L4rQantxDXnpI_w', user_agent='TD3Python')
hot_posts = reddit.subreddit('france').hot(limit=100)
for post in hot_posts:
    texteSubr = post.selftext
    texteSubr = texteSubr.replace("\n", " ")
    if len(texteSubr) >= 20:
        docs.append(texteSubr)
        docs_bruts.append(('Reddit', post))

        

# Récupération des documents de Arxiv
query = "france"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()
data = url_read.decode()
dico = xmltodict.parse(data)
arxivArticle = dico['feed']['entry']

for i, entry in enumerate(arxivArticle):
    if len(entry["summary"]) >= 20:
        docs.append(entry["summary"].replace("\n", ""))
        docs_bruts.append(("ArXiv", entry))


# # Extraction des textes des dictionnaires
# textes = [doc['texte'] for doc in docs]

# # Création d'une unique chaîne de caractères
# corpus_string = ' '.join(textes)
 
longueChaineDeCaracteres = " ".join(docs)
print(docs)

allDocObj = []


for origine, doc in docs_bruts : 
    #Création d'un objet Document venant d'un post Reddit
    if origine == "Reddit" :
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        docObj = Document(titre, auteur, date, url, texte)

        allDocObj.append(docObj)
    
    elif origine == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #Création d'un objet Document venant d'un article Arxiv
        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

        docObj = Document(titre, authors, date, doc["id"], summary)  # Création du Document
        allDocObj.append(docObj)  # Ajout du Document à la liste.

# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(allDocObj):
    id2doc[i] = doc.titre

#Création d'un dictionnaire id2author poru attrribuer a chaque auteur un identifiant unique
authors = {}
aut2id = {}
id_auteurs_unique = 0

# Création de la liste+index des Auteurs
for doc in allDocObj:#On parcours les auteurs de chaque document 
    if doc.auteur not in aut2id: 
        id_auteurs_unique += 1 #On génère l'id de l'auteur en ajoutant 1 à chaque fois qu'on croise un nouvel auteur
        authors[id_auteurs_unique] = Author(doc.auteur)#Création d'un objet dans la liste authors
        aut2id[doc.auteur] = id_auteurs_unique #on ajoute sont id dans la liste indexée

    authors[aut2id[doc.auteur]].add(doc.texte) #pour chaque document écris par cet auteur, on l'ajoute dans son nb de production


#affichage des productions des auteurs et taille moyenne des documents
# for author_id, author_obj in authors.items():
#     print(author_obj)
#     taille_totale_doc = sum(len(doc) for doc in author_obj.production)
#     print(f"taille moyenne des document  : ",taille_totale_doc/author_obj.ndoc)

corpus = Corpus("Mon corpus")
# Construction du corpus à partir des documents
for doc in allDocObj:
    corpus.add(doc)
# corpus.showDocSortedByTitle(len(corpus.id2doc))

# print(repr(corpus))
# corpus.save('corpus.csv')
# corpus_charge = Corpus('CorpusTest')
# corpus_charge.load('corpus.csv')
# print(repr(corpus_charge))























