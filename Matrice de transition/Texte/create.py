# ==============================================================================
"""Generer une matrice de transition en fonction du fichier donné"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "1.0"
__date__    = "2020-02-12"
# ==============================================================================
# coding: utf-8
from music21 import *
from lecture import *
# ------------------------------------------------------------------------------
class Analyse(object):
    """Analyser un fichier midi entre pour en ressortir une matrice de transition"""
    def __init__(self, fichier:str):
        """Initialisation des variables et creation d'un fichier"""
        self.__fichier = fichier
        self.write_start() ; self.decomposition_notes() 

    def write_start(self):
        """Ecriture de l'entete du fichier txt"""
        with open("matrice_de_transition.txt", "w") as fichier_text:    # Gere l'ouverture et la fermeture du fichier
            for i in range(100): fichier_text.write("#")                # Genere une ligne de 100 #
            fichier_text.write("\n########################### Matrice de transition pour " + self.__fichier + " ###########################") 
        self.write_comment()                                            # Genere une ligne de 100 #

    def write_saut(self):
        """Effectuer des sauts de ligne (retour a la ligne)"""
        with open("matrice_de_transition.txt", "a") as fichier_text: fichier_text.write('\n')

    def write_comment(self):
        """Ecrire une ligne de #"""
        with open("matrice_de_transition.txt", "a") as fichier_text:
            fichier_text.write("\n") ; 
            for i in range(100): fichier_text.write("#")

    def write_matrice(self, notes, tuple_notes):
        """Ecriture d'une ligne de la matrice"""
        with open("matrice_de_transition.txt", "a") as fichier_text:
            fichier_text.write("\n("+ str(notes) + ": " + str(tuple_notes[1]) + ")")    # Pour la note x les proba associe
            fichier_text.write("    Pour " + str(notes) + " a n+1 il y a les notes suivantes " + str(tuple_notes[0]))   # Commentaire sur les notes de la ligne

    def write_matrice_info(self):
        """Ecriture des informations concernant la matrice"""
        self.write_saut() ; self.write_comment()
        with open('matrice_de_transition.txt', 'a') as fichier_text:
            fichier_text.write("\nLa liste de notes est : " + str(self.__notes))    # Liste des notes du morceau
        self.write_comment() ; self.write_saut()


    def load(self):
        """Charger le fichier entre"""
        return converter.parse(self.__fichier) # corpus.parse('bach/bwv66.6')

    def decomposition_pistes(self):
        """On decompose le morceau en plusieurs si necessaire"""
        morceau = self.load() 
        tracks = []

        for pistes in morceau.recurse().parts: tracks.append(pistes)    # On separe les pistes (les différents instruments)
        return tracks

    def decomposition_notes(self):
        """Decomposition des pistes en une liste contenant les notes de ces pistes"""
        track = self.decomposition_pistes() ; notes_track =[]

        for pistes in track:    # On parcourt toute la liste des pistes
            notes_track.append([])  # On cree une liste dans une liste qui va contenir les notes d'une piste

            for note_i in range(len(pistes.recurse().notesAndRests)):   # On parcourt toute la piste de notes, d'accords et de silence
                if pistes.recurse().notesAndRests[note_i].isChord == True:  # Si la note est un accord alors
                    note_chord = pistes.recurse().notesAndRests[note_i].notes ; name_chord = '' # On regarde les notes de cet accord

                    for i in range(len(note_chord)): name_chord += ';'+str(note_chord[i].nameWithOctave) # On ajoute cette accord a notre liste de liste
                    notes_track[-1].append(name_chord)

                elif pistes.recurse().notesAndRests[note_i].isRest == True: notes_track[-1].append('rest')  # Si la note est un silence alors on rajoute a la liste de liste le mot silence

                else: notes_track[-1].append(str(pistes.recurse().notesAndRests[note_i].nameWithOctave))    # Si la note est une note lambda alors on l'ajoute a notre liste de liste
            self.analyse(notes_track[-1])   # Lorsque notre liste de liste est rempli on va l'analyser

    def decomposition_dict(self, ligne):
        """Transformer notre dictionnaire en une liste comportant les proba associe aux notes"""
        note_list = list(ligne.values())
        for i in range(len(note_list)): note_list[i] = note_list[i]/sum(ligne.values())
        return (list(ligne.keys()), note_list)

    def analyse(self, notes):
        """Compter les notes au rang n+1"""
        self.__notes = list(set(notes)) ; self.write_matrice_info()
        for i in range(len(self.__notes)):
            ligne = {}
            for j in range(len(notes)-1):
                if self.__notes[i] == notes[j]:
                    if notes[j+1] in ligne: ligne[notes[j+1]] += 1
                    else: ligne[notes[j+1]] = 1
            self.write_matrice(self.__notes[i], self.decomposition_dict(ligne))

# ------------------------------------------------------------------------------
# ==============================================================================
if __name__ == '__main__':
  Analyse(str(input("Nom du fichier a analyser : ")))
# ==============================================================================