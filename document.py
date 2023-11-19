import pandas as pd
# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", type="Type de doc"):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type

#Méthode qui affiche toutes les infos d'un Document
    def __info__(self) :
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    
    def __str__(self) :
        return f"{self.titre}, par {self.auteur}"
    
    def getType(self) : 
        return self.type
    
class RedditDocument(Document) :
    def __init__(self, titre, auteur, date, url, texte):
        super().__init__(titre, auteur, date, url, texte, type="Reddit")
        self.nbCom = 0
    
    def getnumCom(self) :
        return self.nbCom
    def setnbCom(self, nbCom) :
        self.nbCom = nbCom

    def __str__(self):
        return super().__str__() + f" Nombre de commentaires :{self.nbCom}\n {self.getType()}"
    
class ArxivDocument(Document) :
    def __init__(self, titre, auteur, date, url, texte):
        super().__init__(titre, auteur, date, url, texte, type="Arxiv")
        if isinstance(self.auteur, list) :
            self.coAuteur = self.auteur[1:]
            self.auteur = self.auteur[0]
        else :
            self.coAuteur = 0
            
    def __str__(self):
        return super().__str__() + f" Co-Auteurs : {self.coAuteur}\n {self.getType()}"
    


    
    
    