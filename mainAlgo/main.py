from fonctions_utiles import vraisemblance
import scipy
import json

class Main():
    """Moteur de l'algorithme de recommendation 'Apprentissage adaptatif'    """

    #--------------------------------------------------------------------------
    
    def __init__(self, etudiants, themes, competences, exercices, jsonFileName=""):
        self.etudiants = etudiants
        self.themes = themes
        self.competences = competences
        self.exercices = exercices
        self.questions = exercices    ## !
        self.jsonFileName = jsonFileName
        if jsonFileName != "":
            self.chargerJson()
 
        
    
    #--------------------------------------------------------------------------

    def genererQuiz(self, eleve, competencesTestees):
        """Génère une Feuille d'Exercices correspondant à un élève et à des compétences"""
        
        
        fe = []
                      
        # compétences requises
        competencesRequises = []
        for c in competencesTestees:
                if (not c in competencesRequises) and (eleve.getNiveau(c.getId())<=1):
                    competencesRequises.append(c)
        
        
        # generation triviale avec 1 exercice par competence
        for c in competencesRequises+competencesTestees:
            exo = next(e for e in self.exercices if c in e.competences)
            if not exo in fe:
                fe.append(exo)

        
        return fe
        
        
    #--------------------------------------------------------------------------


    def actualiserNiveaux(self, etudiant):
        questions = [self.questions[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
        reponses = [etudiant.questionsRepondues[i] for i in etudiant.questionsRepondues if etudiant.questionsRepondues[i]!=-1]
        diff = [q.difficulte for q in questions]
        matriceQ = [[1 if k in q.competences else 0 for k in self.competences] for q in questions]
        
        f = lambda x : -vraisemblance(questions, x[0], x[1:], diff, matriceQ, reponses)
        niveaux = scipy.optimize.minimize(f, [0]*(len(self.competences)+1))
        print(niveaux.x)
        print(-niveaux.fun)
        etudiant.setCapacite(niveaux.x[0])
        etudiant.setNiveaux(list(niveaux.x[1:]))
        
    
    

    #--------------------------------------------------------------------------
        
    def chargerJson(self):
        """Charge les données depius le(s) fichier(s) json"""
        pass
		
    #-------------------------------------------------------------------------

    #--------------------------------------------------------------------------
        
    def ecrireJson(self):
        """Ecrit les données depius le(s) fichier(s) json"""
        json.dumps(self.exercices, indent=4)
		
    #-------------------------------------------------------------------------

 
    #--------------------------------------------------------------------------
        
    def ajouterExercice(self, exercice):
        """Ajoute un exercice à la base de donnée"""
        pass
		
    #-------------------------------------------------------------------------


        
#==============================================================================

if __name__ == "__main__":
    
    import question, theme, competence, etudiant


    theme1 = theme.Theme(1, "Arithmétique")
    competence1 = competence.Competence(1, "Addition", theme1, [])
    competence2 = competence.Competence(2, "Soustraction", theme1, [competence1])
    competence3 = competence.Competence(3, "", theme1, [])

    bob = etudiant.Etudiant("John", "Smith", [0, 0], 0)
	
    
    q0 = question.Question(0, "3 + 4 =", "7", [theme1], [competence1])
    q1 = question.Question(1, "2 + 5 =", "7", [theme1], [competence1])
    q2 = question.Question(2, "", "", [theme1], [competence2])
    q3 = question.Question(3, "", "", [theme1], [competence2])
    q4 = question.Question(4, "", "", [theme1], [competence1, competence2])
    q5 = question.Question(5, "", "", [theme1], [competence1, competence2])
    q6	= question.Question(6, "", "", [theme1], [competence3])
    
    
    main = Main([bob], [theme1], [competence1, competence2, competence3], [q0,q1,q2,q3,q4,q5,q6])
    
    
    
    
    
#    fe1 = main.genererQuiz(john, [competence1])
#    fe2 = main.genererQuiz(john, [competence2])
#
#    print("FE Addition")
#    for exo in fe1:
#        exo.afficherEnonce()
#    print("FE Soustraction")
#    for exo in fe2:
#        exo.afficherEnonce()
        
   ## main.ecrireJson()