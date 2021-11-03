# ==============================================================================
"""Creer une melodie a partir d'une matrice de transition donnee"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "1.0"
__date__    = "2020-02-22"
# ==============================================================================
import numpy
from music21 import *
# ------------------------------------------------------------------------------
class Melodie(object):
    """Creer la melodie avec une matrice de transition"""
    def __init__(self):
        # Ecrire sa matrice de transition manuellement ici
        # Somme ligne == 1 Oblige
        self.__matrice_proba = {
            "B5":[0,0.09,0.45,0,0.09,0,0,0,0,0,0,0,0.37,0,0],
            "D6":[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            "G5":[0.41,0.08,0,0.16,0,0.25,0,0,0.1,0,0,0,0,0,0],
            "E5":[1/3,0,2/3,0,0,0,0,0,0,0,0,0,0,0,0],
            "A5":[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
            "F#5":[0,0,0.42,0.42,0,0,0,0,0,0.16,0,0,0,0,0],
            "F5":[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
            "C#6":[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            "C6":[0.6,0,0,0,0,0,0,0,0,0,0,0,0,0.4,0],
            "D5":[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
            "rest":[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
            "B4":[0.25,0,0,0.5,0,0,0,0,0,0,0,0.25,0,0,0],
            "B-5":[0,0,0,0,0,0.75,0,0,0,0,0,0,0,0,0.25],
            "G#5":[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            "B-4":[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
        }  
        # Changer les temps (pas nécessaire)
        self.__temps_proba = {1: [0.75,0.25], 2:[1,0]}

        self.__proba_note = self.__matrice_proba[numpy.random.choice(self.notes)] ; self.__proba_temps = self.__temps_proba[numpy.random.choice(self.temps)]

        self.loop();
# ------------------------------------------------------------------------------
    @property
    def notes(self):
        '''Retourne notre liste de notes'''
        return tuple(self.__matrice_proba.keys())
# ------------------------------------------------------------------------------
    @property
    def temps(self):
        """Retourne liste de temps"""
        return tuple(self.__temps_proba.keys())
# ------------------------------------------------------------------------------
    @property
    def notes_pro(self):
        """Tire la note suivante suivant la note precedente"""
        return numpy.random.choice(self.notes, p = self.__proba_note)
# ------------------------------------------------------------------------------
    @property
    def temps_pro(self):
        """Tire le temps suivante suivant le temps precedente"""
        return numpy.random.choice(self.temps, p = self.__proba_temps)
# ------------------------------------------------------------------------------
    def accord(self, accord):
        """Decompose les notes des accords"""
        return accord[1:].split(";")
# ------------------------------------------------------------------------------
    def loop(self):
        """Genere le morceau"""
        morceau = stream.Stream() # Ouverture d'un flux (stream)
        for i in range(1,10): # On fait 10 mesures (changez si vous le souhaitez)
            longueur = 0 ; mesure = stream.Stream() ; mesure = stream.Measure(number = i) # Def de notre mesure
            while longueur < 4: # Tant que la mesure n'est pas rempli
                
                note_tirer = self.notes_pro # on tire soit une note/accord/silence

                if ";" in note_tirer: note_mesure = chord.Chord(self.accord(note_tirer))  # Si c'est un accord on decompose le str
                elif note_tirer == "rest": note_mesure = note.Rest() # Si c'est un silence
                else: note_mesure = note.Note(note_tirer) # Si c'est une note 'normale'

                note_mesure.duration.quarterLength = self.temps_pro.astype(float) # Le temps de la note ou silence ou accord

                self.__proba_note = self.__matrice_proba[note_tirer] ; self.__proba_temps = self.__temps_proba[note_mesure.duration.quarterLength] # On se place à l'etat i de la matrice de transition
                longueur += note_mesure.duration.quarterLength ; mesure.append(note_mesure) # On augmente 

            morceau.insert(mesure) # On insere la mesure au flux
        morceau.show() # On montre le morceau sur MuseScore ou mettre 'midi' et ça affichera sur votre lecteur par defaut
# ------------------------------------------------------------------------------
# ==============================================================================
if __name__ == '__main__':
  Melodie()
# ==============================================================================
