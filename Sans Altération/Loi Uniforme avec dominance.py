# ==============================================================================
"""Generer une mélodie aléatoirement centre en la dominante"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "1.0"
__date__    = "2020-01-22"
# ==============================================================================
from random import *
from music21 import *
# ------------------------------------------------------------------------------
class Uniform(object):
    def __init__(self):
        """Creation de notre univers de notes"""
        self.__notes = []
        for i in range(4,5):
            for j in 'CDEFGAB':
                self.__notes.append(str(j)+str(i))
##        self.__temps_number = [1/(2**i) for i in reversed(range(3,7))]
##        self.__temps = ['64th', '32nd', '16th', "eighth", 'quarter', 'half', 'whole']
##        self.__temps = ["eighth", 'quarter', 'half', 'whole']

        self.loop() ;
# ------------------------------------------------------------------------------
    def dominante(self, choix):
        """Centre la note en la dominante"""
        gamme = 'CDEFGABCDEFGAB'                                    # Possibilité des notes facilite la suite du code
        octave = int(choix[1])                                      # On stocke l'octave de la note genere au debut
        self.__notes = []                                           # On reinitiale les notes qu'on a
        for i in range(len(gamme)):                                 # On parcours la liste des gammes
            if gamme[i] == choix[0]:                                # Si elle correspond à la note genere precedamment
                separ = gamme.split(gamme[i])                       # On separe la chaine de caractere et on les stocke dans une liste
                gamme = separ[1] + choix[0]                         # Alors on supprime les elements qui precede i de la gamme
                for j in range(len(gamme)):                         # Puis on reparcours la liste des gammes 
                    if gamme[j] == "C":                             # Puis la note est DO alors on augmente l'octave
                        octave += 1                                 # On augmente l'octave
                    if j <= 3:                                      # Pour les probabilite
                        for k in range(j+1):                        # On copie j fois la note dans la liste
                            self.__notes.append(str(gamme[j])+str(octave))
                            
                    else:                                           # Sinon on fais l'inverse on copie le nombre de fois que la derniere note de la liste -1
                        k = self.__notes.count(self.__notes[-1]) - 1
                        for l in range(k):
                            self.__notes.append(str(gamme[j])+str(octave))
                    if gamme[j]== choix[0]:                         #Si la note est egale a la note genere au debut 
                        break                                       # Alors on arrete tout
            if len(self.__notes) != 0:
                break
# ------------------------------------------------------------------------------
    def choix(self):
        """Renvoie un silence ou une note avec une proba fixe 1/10 pour le silence"""
        a = ['note', 'note', 'note', 'note', 'note', 'note', 'note', 'note', 'note', 'silence']
        return a[randint(0,len(a)-1)]
# ------------------------------------------------------------------------------
    def notes(self):
        """Renvoie la valeur de la note"""
        return self.__notes[randint(0, len(self.__notes)-1)]
# ------------------------------------------------------------------------------
    def temps(self):
        """Renvoie la duree de la note avec une equiprobabilité"""
        return self.__temps[randint(0, len(self.__temps)-1)]
# ------------------------------------------------------------------------------
    def loop(self):
        """Creation d'un morceau sur 4 mesures"""
        morceau = stream.Stream()
        self.dominante(self.notes())                                        # On genere une nouvelle palette de notes centre en la dominante
        
        for i in range(1,5):
            longueur = 0            
            mesure = stream.Stream()                                        # Ouverture d'un flux permettant de stocker les notes
            mesure = stream.Measure(number=i+1)                             # Travail sur la mesure i+1
            self.__temps_number = [1/(2**i) for i in reversed(range(-2,2))] # Liste sur la duree des notes
            self.__temps = ["eighth", 'quarter', 'half', 'whole']           # Meme chose mais avec des chaines de caracteres
            while longueur < 4:                                             # Tant que la mesure n'est pas complete
                if longueur + self.__temps_number[-1] > 4:                  # Si la duree de la valeur de la note est superieure à 4
                    del self.__temps[-1]                                    # Alors on supprime la derniere duree
                    del self.__temps_number[-1]                             # Pareil
                n_ou_s = self.choix()                                       # On tire une note ou un silence
                if n_ou_s == 'note':                                        # Si c'est une note
                    note_morceau = note.Note(self.notes())                  # On tire la valeur de la note
                    note_morceau.duration.type = self.temps()               # Puis sa duree
                else:                                                       # Sinon si c'est un silence
                    note_morceau = note.Rest()                              # On dit que la valeur de la 'note' est un silence
                    note_morceau.duration.type = self.temps()               # Puis on associe a cette valeur une duree
        
                for i in range(len(self.__temps)):                          # On cree une boucle qui parcours la liste qui contient les duree
                    if self.__temps[i] == note_morceau.duration.type:       # Si la duree correspond à celle qu'on a tire precedamment
                        mesure.append(note_morceau)                         # On rajoute la note dans la mesure
                        longueur += self.__temps_number[i]                  # Puis on incremente la duree de la note a la variable longueur
                        
            morceau.insert(mesure)                                          # Une fois la mesure termine rajoute cette derniere dans notre morceau
        morceau.show()                                                      # Nous montre sur musescore le morceau generé
# ------------------------------------------------------------------------------            
# ==============================================================================
if __name__ == '__main__':
  Uniform()
# ==============================================================================
