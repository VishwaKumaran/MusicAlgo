# ==============================================================================
"""Creer une melodie a partir d'une matrice de transition donnee"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "2.0"
__date__    = "2020-02-22"
# ==============================================================================
from music21 import *
import numpy
from fractions import Fraction
from lxml import etree
# ------------------------------------------------------------------------------
class Read_notes(object):
    """Lecture du fichier qui contient toutes les notes d'un morceau"""
    def __init__(self, fichier = "matrice_de_transition_notes.xml"):
        self.__fichier = fichier ; self.__matrice_proba = []

    @property
    def matrice_note(self): return self.__matrice_proba # Retourne la matrice de transition des notes

    @property
    def open_file(self): return etree.parse(self.__fichier).getroot()   # Ouvre le fichier xml 

    @property
    def nombre_decomposition_morceau(self): return len(self.__morceau.findall('matrice'))   # Compte le nombre de partitions present dans le fichier

    @property
    def list_notes(self):
        """Nous donne la gamme de note que contient les differentes partitions"""
        list_notes = []
        for notes in self.__morceau.xpath("//matrice[@id = '{}']/longueur/note".format(self.__i)): list_notes.append(notes.text) 
        return list_notes

    @property
    def path_info_ligne_note(self): return self.__morceau.xpath("//matrice[@id = '{}']/ligne[@note_actu='{}']/ligne_note/note".format(self.__i, self.__note_actu)) # C'est un chemin dans le fichier xml

    @property
    def path_info_ligne_text(self): return self.__morceau.xpath("//matrice[@id = '{}']/ligne[@note_actu='{}']/ligne_info/text".format(self.__i, self.__note_actu)) # C'est un chemin dans le fichier xml
    
    @property
    def info_ligne_text(self):
        """Prend les informations manuscrite dans le fichier xml"""
        info = []
        for i in self.path_info_ligne_text: info.append(i.text)
        return info

    def start(self):
        """Ouverture du fichier et decomposition de ce dernier pour obtenir les pistes"""
        self.__morceau = self.open_file ; self.__nb_partitions = self.nombre_decomposition_morceau
        for self.__i in range(1, self.__nb_partitions+1): self.read()

    def assemblage(self):
        """On assemble notre ligne de matrice"""
        note_transition = [] # etat i de la matrice 
        for notes in self.list_notes:
            try: note_transition.append(str(self.path_info_ligne_note[self.info_ligne_text.index(notes)].text)) # si la note existe ecrire sa proba
            except: note_transition.append(0) # Sinon mettre 0

        return note_transition

    def read(self):
        """Constition de la matrice"""
        self.__matrice_proba.append({})
        for self.__note_actu in self.list_notes: 
            self.__matrice_proba[-1][self.__note_actu] = self.assemblage()


class Read_temps(object):
    """docstring for Read_temps"""
    def __init__(self, fichier = "matrice_de_transition_temps.xml"):
        self.__fichier = fichier ; self.__matrice_proba = []

    @property
    def matrice_temps(self): 
        #print(self.__matrice_proba)
        return self.__matrice_proba

    @property
    def list_temps(self):
        list_temps = []
        for temps in self.__morceau.xpath("//matrice[@id='{}']/longueur/note".format(self.__i)): list_temps.append(temps.text)
        return list_temps
    
    @property
    def path_info_ligne_temps(self): return self.__morceau.xpath("//matrice[@id = '{}']/ligne[@temps_actu='{}']/ligne_temps/note".format(self.__i, self.__temps_actu))

    @property
    def path_info_ligne_temps_text(self): return self.__morceau.xpath("//matrice[@id = '{}']/ligne[@temps_actu='{}']/ligne_info/text".format(self.__i, self.__temps_actu))
    
    @property
    def info_ligne_temps(self):
        info = []
        for i in self.path_info_ligne_temps_text: info.append(i.text)
        return info

    def first(self): 
        self.__morceau = etree.parse(self.__fichier).getroot() 
        for self.__i in range(1, len(self.__morceau.findall('matrice'))+1): self.analyse()

    def analyse(self):
        self.__matrice_proba.append({})
        for self.__temps_actu in self.list_temps: self.__matrice_proba[-1][self.__temps_actu] = self.complete()

    def complete(self):
        temps_transition = []
        for temps in self.list_temps:
            try: temps_transition.append(str(self.path_info_ligne_temps[self.info_ligne_temps.index(temps)].text))
            except: temps_transition.append(0)

        return temps_transition    
    
class Melodie(Read_notes, Read_temps):
    """Creer la melodie avec une matrice de transition"""
    def __init__(self):
        Read_notes.__init__(self)
        Read_temps.__init__(self) 

        self.start() ; self.first()

        self.__morceau = stream.Score(id='Main')

        for self.__i in range(len(self.matrice_note)): self.loop();
        self.__morceau.show()

    @property
    def notes(self):
        return tuple(self.matrice_note[self.__i].keys())

    @property
    def temps(self):
        return tuple(self.matrice_temps[self.__i].keys())

    @property
    def notes_pro(self):
        return numpy.random.choice(self.notes, p = self.fraction(self.__proba_note))

    @property
    def temps_pro(self):
        return numpy.random.choice(self.temps, p = self.fraction(self.__proba_temps))

    def fraction(self, proba):
        fraction_list = []
        for i in proba: fraction_list.append(Fraction(i))
        return fraction_list

    def accord(self, accord):
        return accord[1:].split(";")

    def loop(self):
        self.__proba_note = self.matrice_note[self.__i][numpy.random.choice(self.notes)] ; self.__proba_temps = self.matrice_temps[self.__i][numpy.random.choice(self.temps)]
        
        part = stream.Part(id='part{}'.format(self.__i))
        for i in range(1,50):
            longueur = 0 ; mesure = stream.Stream() ; mesure = stream.Measure(number = i)
            while longueur < 4:
                # Ajouter une condition si le temps pris est superieur a 4 temps 
                
                note_tirer = self.notes_pro

                if ";" in note_tirer: note_mesure = chord.Chord(self.accord(note_tirer)) 
                elif note_tirer == "rest": note_mesure = note.Rest()
                else: note_mesure = note.Note(note_tirer)

                note_mesure.duration.quarterLength = float(Fraction(self.temps_pro)) ; 

                self.__proba_note = self.matrice_note[self.__i][note_tirer] ; self.__proba_temps = self.matrice_temps[self.__i][str(note_mesure.duration.quarterLength)]
                longueur += note_mesure.duration.quarterLength ; mesure.append(note_mesure)

            part.append(mesure)
        self.__morceau.insert(part)
# ------------------------------------------------------------------------------
# # ==============================================================================
# if __name__ == '__main__':
#   Melodie()
# # ==============================================================================
