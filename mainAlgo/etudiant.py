
class Etudiant():
    """Représentation d'un étudiant et de ses capacités    """

    def __init__(self, prenom, nom, niveauxCompetences=[], capacite=0):
        self.prenom = prenom
        self.nom = nom
        self.niveauxCompetences = niveauxCompetences ## [theta_1, theta_2, ...]
        self.capacite = capacite
        self.questionsRepondues = {} ## {question.idNb: -1 non repondue, 0 faux ou 1 juste, ...}
        
    def getNiveau(self, competenceId):
        return self.niveauxCompetences[competenceId]
        
    def setNiveaux(self, niveaux):
        self.niveauxCompetences = niveaux
 
    def setCapacite(self, capacite):
        self.capacite = capacite
        

    def getCapacites(self):
        return self.capacite, self.niveauxCompetences
    

        
