class Main():
    """Fonction principale de l'algorithme de recommendation 'Apprentissage adaptatif'    """

    #--------------------------------------------------------------------------
    
    def __init__(self, etudiants, themes, competences, exercices):
        self.listeEtudiants = etudiants
        self.listeThemes = themes
        self.listeCompetences = competences
        self.listeExercices = exercices
        
    
    #--------------------------------------------------------------------------

    def genererFE(self, eleve, theme, nbExercices=3):
        """Génère une Feuille d'Exercices correspondant à un élève et à un 
        thème"""
        
        fe = []
        
        # generation triviale
        i = 0
        while len(fe)<=nbExercices and (i+1)<len(self.listeExercices):
            exo = self.listeExercices[i]
			for t in exo.themes:
                if t.nbId == theme.nbId:
                    fe.append(exo)
            i+=1
            
        return fe
        
        
    #--------------------------------------------------------------------------
 

 
    #--------------------------------------------------------------------------
        
    def ajouterExercice(exercice):
        """Ajoute un exercice à la base de donnée"""
		
    #--------------------------------------------------------------------------


        
#==============================================================================

if __name__ == "__main__":
    
    import exercice, theme, competence, etudiant

    john = etudiant.Etudiant("John", "Smith", [0, 0])

    theme1 = theme.Theme(1, "Arithmétique")
    competence1 = competence.Competence(1, "Addition", theme1)
    competence2 = competence.Competence(2, "Soustraction", theme1)
	
    
    ex1 = exercice.Exercice(1, "", ["3 + 4 ="], ["7"], [theme1], [competence1])
    ex2 = exercice.Exercice(2, "", ["2 + 5 ="], ["7"], [theme1], [competence1])
    ex3 = exercice.Exercice(3, "", ["6 + 6 ="], ["12"], [theme1], [competence1])
    ex4	= exercice.Exercice(4, "", ["6 - 2 ="], ["4"], [theme1], [competence2])
    
    
    main = Main([john], [theme1], [competence1, competence2], [ex1, ex2, ex3, ex4])
    fe = main.genererFE(john, theme1)

    for exo in fe:
        exo.afficherEnonce()