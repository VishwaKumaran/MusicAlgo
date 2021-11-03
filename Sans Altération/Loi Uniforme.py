# ==============================================================================
"""Generer une mélodie aléatoirement avec une loi uniforme"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "2.0"
__date__    = "2020-02-05"
# ==============================================================================
from random import *
from music21 import *
import numpy
# ------------------------------------------------------------------------------
class Uniform(object):
    def __init__(self):
        """Creation de notre univers de notes"""
        self.__notes, self.__proba = [], []
        for i in range(4,5):
            for j in 'CDEFGAB':
                self.__notes.append(str(j)+str(i))

        for i in range(len(self.__notes)):
            self.__proba.append(1/len(self.__notes))

        """On cree une palette de note qui va de C4 et C5"""
##        self.__temps_number = [1/(2**i) for i in reversed(range(3,7))]
##        self.__temps = ['64th', '32nd', '16th', "eighth", 'quarter', 'half', 'whole']
##        self.__temps = ["eighth", 'quarter', 'half', 'whole']

        self.loop() ;
# ------------------------------------------------------------------------------
    def choix(self):
        """Renvoie un silence ou une note avec une proba fixe 1/10 pour le silence"""
        return numpy.random.choice(['note', 'silence'], p=[9/10,1/10])
# ------------------------------------------------------------------------------
    def notes(self):
        """Renvoie la valeur de la note avec une equiprobabilité"""
        return numpy.random.choice(self.__notes, p=self.__proba)
# ------------------------------------------------------------------------------
    def temps(self):
        """Renvoie la duree de la note avec une equiprobabilité"""
        proba_temps = []
        for i in range(len(self.__temps)):
            proba_temps.append(1/len(self.__temps))

        return numpy.random.choice(self.__temps, p=proba_temps)
# ------------------------------------------------------------------------------
    def loop(self):
        """Creation d'un morceau sur 4 mesures"""
        morceau = stream.Stream()                                           # Ouverture d'un flux qui va permettre de stocker notre morceau
        for i in range(1,5):                                                # On va creer un morceau sur 4 morceaux
            longueur = 0
            mesure = stream.Stream()                                        # Ouverture d'un flux permettant de stocker les notes
            mesure = stream.Measure(number=i)                               # Travail sur la mesure , number i
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
                        
            morceau.insert(mesure)                                          # Une fois la mesure termine rajoute cette derniere dans notre 
        morceau.show()                                                      # Nous montre sur musescore le morceau generé
# ------------------------------------------------------------------------------            
# ==============================================================================
if __name__ == '__main__':
  Uniform()
# ==============================================================================
