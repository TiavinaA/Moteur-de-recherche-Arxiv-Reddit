import praw
import urllib
import xmltodict
import pandas as pd

docs = []

#Récupération des documents de Reddit
reddit = praw.Reddit(client_id='nzJcQWMzVE8P6uYYll0-Bg', client_secret='s3M97y4jzMOiNr1L4rQantxDXnpI_w', user_agent='TD3Python')
hot_posts = reddit.subreddit('france').hot(limit=100)
for post in hot_posts:
    titreSubr = post.selftext
    titreSubr = titreSubr.replace("\n", " ")
    if len(titreSubr) >= 20:
        docs.append({'identifiant': len(docs) + 1, 'texte': titreSubr, 'origine': 'reddit'})

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

#Mise en forme des données dans un DataFrame
allArticlesDf = pd.DataFrame(docs, columns=['identifiant', 'texte', 'origine'])

allArticlesDf.to_csv('corpusTD3.csv', sep='\t', index=False)

# Extraction des textes des dictionnaires
textes = [doc['texte'] for doc in docs]

# Création d'une unique chaîne de caractères
corpus_string = ' '.join(textes)









