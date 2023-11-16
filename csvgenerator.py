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

        #Afficher les attributs des Docs Reddit
# for i, post in enumerate(hot_posts):
#  # Pour connaître les différentes variables et leur contenu
#         for k, v in post.__dict__.items():
#             pass
#             print(k, ":", v)
#         break    
        

# Récupération des documents de Arxiv
query = "france"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()
data = url_read.decode()
dico = xmltodict.parse(data)
arxivArticle = dico['feed']['entry']
for article in arxivArticle :
    texte = article['summary']
    texte = texte.replace("\n", " ")
    if len(texte) >= 20:
        docs.append({'identifiant': len(docs) + 1, 'texte': texte, 'origine': 'arxiv'})

# #Mise en forme des données dans un DataFrame
# allArticlesDf = pd.DataFrame(docs, columns=['identifiant', 'texte', 'origine'])

# allArticlesDf.to_csv('corpusTD3.csv', sep='\t', index=False)

# # Extraction des textes des dictionnaires
# textes = [doc['texte'] for doc in docs]

# # Création d'une unique chaîne de caractères
# corpus_string = ' '.join(textes)

allDocObj = []

#Création d'un objet Document venant d'un post Reddit
for origine, doc in docs_bruts : 
    if origine == "Reddit" :
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        docObj = Document(titre, auteur, date, url, texte)

        allDocObj.append(docObj)











