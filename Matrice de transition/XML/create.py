# ==============================================================================
"""Generer une matrice de transition en fonction du fichier donné"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "2.0"
__date__    = "2020-02-26"
# ==============================================================================
from music21 import *
import numpy
from fractions import Fraction
from lxml import etree
from lecture import *
# ------------------------------------------------------------------------------
class Analyse(object):
    """Analyser un fichier midi entre pour en ressortir une matrice de transition"""
    def __init__(self, fichier:str):
        """Initialisation des variables et creation d'un fichier"""
        self.__fichier = fichier ; self.__data = [] ; self.__temps_data = [] ; self.__i = 0 

    @property
    def load(self):
        """Charger le fichier entre"""
        return converter.parse(self.__fichier) # corpus.parse('bach/bwv66.6')

    def decomposition_pistes(self):
        """On decompose le morceau en plusieurs si necessaire"""
        morceau = self.load ; tracks = []
        for pistes in morceau.recurse().parts: tracks.append(pistes)    # On separe les pistes (les différents instruments)
        return tracks

    def decomposition_notes(self):
        """Decomposition des pistes en une liste contenant les notes de ces pistes"""
        track = self.decomposition_pistes() ; notes_track =[] ; liste_temps = [] ; 

        for pistes in track:    # On parcourt toute la liste des pistes
            notes_track.append([]) ; liste_temps.append([]) ; self.__i+=1  # On cree une liste dans une liste qui va contenir les notes d'une piste

            for note_i in range(len(pistes.recurse().notesAndRests)):   # On parcourt toute la piste de notes, d'accords et de silence
                liste_temps[-1].append(pistes.recurse().notesAndRests[note_i].quarterLength)

                if pistes.recurse().notesAndRests[note_i].isChord == True:  # Si la note est un accord alors
                    note_chord = pistes.recurse().notesAndRests[note_i].notes ; name_chord = '' # On regarde les notes de cet accord

                    for i in range(len(note_chord)): name_chord += ';'+str(note_chord[i].nameWithOctave) # On ajoute cette accord a notre liste de liste
                    notes_track[-1].append(name_chord)

                elif pistes.recurse().notesAndRests[note_i].isRest == True: notes_track[-1].append('rest')  # Si la note est un silence alors on rajoute a la liste de liste le mot silence

                else: notes_track[-1].append(str(pistes.recurse().notesAndRests[note_i].nameWithOctave))    # Si la note est une note lambda alors on l'ajoute a notre liste de liste
            self.analyse(notes_track[-1], self.__i) ; self.analyse_temps(liste_temps[-1], self.__i)  # Lorsque notre liste de liste est rempli on va l'analyser
        

        for i in range(len(self.__data)-1): self.__data[0].extend(self.__data[i+1])     # une fois termine on assemble toutes les partitions
        file_export = self.write_file(self.__data[0]) ; file_export.write("matrice_de_transition_notes.xml")    # et on l'exporte sous forme de fichier xml

        for i in range(len(self.__temps_data)-1): self.__temps_data[0].extend(self.__temps_data[i+1])   # meme chose pour le temps
        file_export = self.write_file(self.__temps_data[0]) ; file_export.write("matrice_de_transition_temps.xml")

    def decomposition_dict(self, ligne):
        """Transformer notre dictionnaire en une liste comportant les proba associe aux notes"""
        note_list = list(ligne.values())    # on recupere toutes les valeurs
        for i in range(len(note_list)): note_list[i] = note_list[i]/sum(ligne.values()) # puis on met sous forme d'une proba
        note_list = self.simplification(note_list)  # ces proba seront transforme en fraction
        return (list(ligne.keys()), note_list)

    def simplification(self, note_ligne):
        """Met sous forme d'une fraction les probas"""
        simple = []
        for i in note_ligne: simple.append(Fraction(i).limit_denominator())
        return simple

    def analyse(self, notes, iteration):
        """Compter les notes au rang n+1"""
        self.__notes = list(set(notes)) ; data = self.write_start ; matrice = self.write_matrice(data) ; matrice.set("id", str(iteration)) ; longueur = self.write_longueur(matrice) ;
        
        for i in range(len(self.__notes)):              # On ecrit toutes la gamme de note dans une variable qui sera plus tard notre fichier xml
            matrice_note = self.write_notes(longueur)
            matrice_note.text = str(self.__notes[i])

        for i in range(len(self.__notes)):  # On met les notes dans un dictionnaire et compte les notes au rang i+1
            ligne = {}
            for j in range(len(notes)-1):
                if self.__notes[i] == notes[j]:
                    if notes[j+1] in ligne: ligne[notes[j+1]] += 1
                    else: ligne[notes[j+1]] = 1

            matrice_ligne = self.write_ligne(matrice) ; matrice_ligne.set("note_actu", str(self.__notes[i])) ; ligne_info = self.decomposition_dict(ligne)

            ligne_note = self.write_ligne_note(matrice_ligne) # On ecrit pour chaque note la proba des notes qui vont suivre au rang n+1
            for i in range(len(ligne_info[1])):
                matrice_note = self.write_notes(ligne_note)
                matrice_note.text = str(ligne_info[1][i])

            matrice_ligne_info = self.write_ligne_info(matrice_ligne)   # Meme chose mais sous forme manuscrite
            for i in range(len(ligne_info[0])):
                matrice_ligne_text = self.write_ligne_text(matrice_ligne_info)
                matrice_ligne_text.text = str(ligne_info[0][i])

        self.__data.append(data)
    
    def analyse_temps(self, temps, iteration):
        """Cette fonction est la même que la precedente (difference: elle traite le temps des notes)"""
        self.__temps = list(set(temps)) ; data = self.write_start ; matrice = self.write_matrice(data) ; matrice.set('id', str(iteration)) ; longueur = self.write_longueur(matrice)
        for i in range(len(self.__temps)):
            matrice_temps = self.write_notes(longueur)
            matrice_temps.text = str(self.__temps[i])

        for i in range(len(self.__temps)):
            ligne = {}
            for j in range(len(temps)-1):
                if self.__temps[i] == temps[j]:
                    if temps[j+1] in ligne: ligne[temps[j+1]] +=1
                    else: ligne[temps[j+1]] = 1 
            if len(ligne) == 0:
                for j in self.__temps:
                    ligne[j] = 1

            matrice_ligne = self.write_ligne(matrice) ; matrice_ligne.set("temps_actu", str(self.__temps[i])) ; ligne_info = self.decomposition_dict(ligne)

            ligne_temps = self.write_ligne_temps(matrice_ligne)
            for i in range(len(ligne_info[1])):
                matrice_temps = self.write_notes(ligne_temps)
                matrice_temps.text = str(ligne_info[1][i])

            matrice_ligne_info = self.write_ligne_info(matrice_ligne)
            for i in range(len(ligne_info[0])):
                matrice_ligne_text = self.write_ligne_text(matrice_ligne_info)
                matrice_ligne_text.text = str(ligne_info[0][i])

        self.__temps_data.append(data)

class Write(Analyse):
    """Ecriture dans un fichier xml"""
    def __init__(self):
        super().__init__(str(input("Nom du fichier a analyser : ")))
        self.decomposition_notes() # On appelle la fonction

    @property   
    def write_start(self): return etree.Element("root") # On ecrit la premiere balise de depart

    def write_matrice(self, variables): return etree.SubElement(variables, 'matrice')   # On met notre balise qui va contenir les differentes partitions

    def write_longueur(self, variables): return etree.SubElement(variables, "longueur") # Elle va contenir toute les notes de la partition

    def write_ligne(self, variables): return etree.SubElement(variables, 'ligne')   # Elle va contenir toutes les infos sur la ligne

    def write_ligne_note(self, variables): return etree.SubElement(variables, "ligne_note") # Toutes les notes au rang n+1 associe a une note i

    def write_ligne_temps(self, variables): return etree.SubElement(variables, "ligne_temps")   # Meme chose mais avec les temps

    def write_ligne_info(self, variables): return etree.SubElement(variables, 'ligne_info') # On met a quoi correspond les notes leurs infos

    def write_notes(self, variables): return etree.SubElement(variables, 'note')  # On met les notes ou temps

    def write_ligne_text(self, variables): return etree.SubElement(variables, 'text')   # On met du text pour comprendre qui est qui

    def write_file(self, variables): return etree.ElementTree(variables)  # Permet d'exporter le fichier xml
# ------------------------------------------------------------------------------
# ==============================================================================
if __name__ == '__main__':
  Write()
  Melodie()
# ==============================================================================
