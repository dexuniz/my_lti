class Exercice():
    """Exercice lambda	"""

    def __init__(self, nId, enonce, questions, reponses, themes, competences):
        self.nId = nId
        self.enonce = enonce
        self.questions = questions
        self.reponses = reponses
        self.themes = themes
        self.competences = competences
	

    def afficherEnonce(self):
        print(self.enonce)
        for q in self.questions:
            print("\n"+q)

		
		
		