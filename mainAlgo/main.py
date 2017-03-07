class Main():
    """Fonction principale de l'algorithme de recommendation 'Apprentissage adaptatif'    """

    #--------------------------------------------------------------------------
    
    def __init__(self, etudiants, themes, competences, exercices):
        self.listeEtudiants = etudiants
        self.listeThemes = themes
        self.listeCompetences = competences
        self.listeExercices = exercices
        
    
    #--------------------------------------------------------------------------

    def genererQuiz(self, eleve, competencesTestees):
        """Génère une Feuille d'Exercices correspondant à un élève et à des compétences"""
        
        
        fe = []
                      
        # compétences requises
        competencesRequises = []
        for c in competencesTestees:
            for cr in c.getPrerequis():
                if (not cr in competencesRequises) and (eleve.niveauCompetences(cr.getId())<=1):
                    competencesRequises.append(cr)
        
        
        # generation triviale avec 1 exercice par competence
        for c in competencesRequises+competencesTestees:
            exo = next(e for e in self.listeExercices if c in e.competences)
            if not exo in fe:
                fe.append(exo)

        
        return fe
        
        
    #--------------------------------------------------------------------------
 

 
    #--------------------------------------------------------------------------
        
    def ajouterExercice(exercice):
        """Ajoute un exercice à la base de donnée"""
        pass
		
    #-------------------------------------------------------------------------


        
#==============================================================================

if __name__ == "__main__":
    
    import exercice, theme, competence, etudiant


    theme1 = theme.Theme(1, "Arithmétique")
    competence1 = competence.Competence(1, "Addition", theme1, [])
    competence2 = competence.Competence(2, "Soustraction", theme1, [competence1])

    john = etudiant.Etudiant("John", "Smith", [0, 0])
	
    
    ex1 = exercice.Exercice(1, "", ["3 + 4 ="], ["7"], [theme1], [competence1])
    ex2 = exercice.Exercice(2, "", ["2 + 5 ="], ["7"], [theme1], [competence1])
    ex3 = exercice.Exercice(3, "", ["6 + 6 ="], ["12"], [theme1], [competence1])
    ex4	= exercice.Exercice(4, "", ["6 - 2 ="], ["4"], [theme1], [competence2])
    
    
    main = Main([john], [theme1], [competence1, competence2], [ex1, ex2, ex3, ex4])
    
    fe1 = main.genererQuiz(john, [competence1])
    fe2 = main.genererQuiz(john, [competence2])

    print("FE Addition")
    for exo in fe1:
        exo.afficherEnonce()
    print("FE Soustraction")
    for exo in fe2:
        exo.afficherEnonce()