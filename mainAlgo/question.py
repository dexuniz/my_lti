class Question():
    """Exercice lambda	"""

    def __init__(self, nId, enonce, reponse, themes, competences, difficulte=1):
        self.nId = nId
        self.enonce = enonce
        self.reponse = reponse
        self.themes = themes
        self.competences = competences
        self.difficulte = difficulte # chaque question a 1 difficulté (il n'y a pas de difficultés différentes pour chaque connaissance)
	

		
		