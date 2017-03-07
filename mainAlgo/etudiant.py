class Etudiant():
    """Représentation d'un étudiant et de ses capacités    """

    def __init__(self, prenom, nom, matriceCompetences=[]):
        self.prenom = prenom
        self.nom = nom
        self.matriceCompetences = matriceCompetences
        self.quiz = []
        
    def niveauCompetences(self, competenceId):
        return self.matriceCompetences[competenceId]
        
    def actualiserNiveau(self, competenceId, niveau):
        self.matriceCompetences[competenceId, niveau]
    
    def ajouterQuizz(self, quiz):
        self.quiz.append(quiz)      
        
        
