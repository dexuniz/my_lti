class Exercice():
    """Exercice lambda	"""

    def __init__(self, nbId, enonce, questions, reponses, themes, competences):
        self.enonce = enonce
        self.questions = questions
        self.reponses = reponses
        self.themes = themes
        self.competences = competences
	

    def afficherEnonce(self):
        print(self.enonce)
        for q in self.questions:
            print("\n"+q)

		
		
		