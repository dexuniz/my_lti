class Competence():
    """Compétence mathémathique
    comme par exemple 'Réduire une fraction'    """

    def __init__(self, nId, texte, theme, competencesRequises):
        self.texte = texte
        self.theme = theme
        self.nId = nId
        self.prerequis = competencesRequises
        
    def getId(self):
        return self.nId

    def getPrerequis(self):
        return self.prerequis
