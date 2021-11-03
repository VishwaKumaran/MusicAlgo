# ==============================================================================
"""Trouver la valeur de reference de la fonction de fitness"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "2.0"
__date__    = "2020-04-08"
# ==============================================================================
from music21 import *
import numpy
from fractions import Fraction
# ------------------------------------------------------------------------------
class Fitness(object):
	"""docstring for Fitness"""
	def __init__(self, fichier:str):
		self.fichier = fichier

	@property
	def load(self): return converter.parse(self.fichier)

	def decomposition(self):
		morceau = self.load ; tracks = []
		for pistes in morceau.recurse().parts: tracks.append(pistes)    # On separe les pistes (les différents instruments)
		return tracks

	def decomposition_notes(self):
		track = self.decomposition() ; notes_track =[] ; liste_temps = [] 

		for pistes in track:    # On parcourt toute la liste des pistes
			notes_track.append([]) ; liste_temps.append([])  # On cree une liste dans une liste qui va contenir les notes d'une piste

			for note_i in range(len(pistes.recurse().notesAndRests)):   # On parcourt toute la piste de notes, d'accords et de silence
				

				if pistes.recurse().notesAndRests[note_i].isChord == True: pass  # Si la note est un accord alors
					# note_chord = pistes.recurse().notesAndRests[note_i].notes ; name_chord = '' # On regarde les notes de cet accord

					# for i in range(len(note_chord)): name_chord += ';'+str(note_chord[i].nameWithOctave) # On ajoute cette accord a notre liste de liste
					# notes_track[-1].append(name_chord)

				elif pistes.recurse().notesAndRests[note_i].isRest == True: pass # notes_track[-1].append('rest')  # Si la note est un silence alors on rajoute a la liste de liste le mot silence

				else: 
					note_temps = pistes.recurse().notesAndRests[note_i].quarterLength
					if note_temps != 0:
						liste_temps[-1].append(note_temps)
						notes_track[-1].append(str(pistes.recurse().notesAndRests[note_i].nameWithOctave))    # Si la note est une note lambda alors on l'ajoute a notre liste de liste
		return {'note':notes_track, 'temps': liste_temps}

	def fitness(self):
		list_notes = self.decomposition_notes() ; total = 0 ; fitness = 0
		def distance(x1, x2):
			list_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
			list_notes_another = ['C', 'D-', 'D', 'E-', 'E', 'F', 'G-', 'G', 'A-', 'A', 'B-', 'B']
			if len(x1)==3:
				if x1[:2] in list_notes: index1 = list_notes.index(x1[:2])
				else: index1 = list_notes_another.index(x1[:2])
			else:
				if x1[0] in list_notes: index1 = list_notes.index(x1[0])
				else: index1 = list_notes_another.index(x1[0])

			if len(x2)==3:
				if x2[:2] in list_notes: index2 = list_notes.index(x2[:2])
				else: index2 = list_notes_another.index(x2[:2])
			else:
				if x2[0] in list_notes: index2 = list_notes.index(x2[0])
				else: index2 = list_notes_another.index(x2[0])
				
			return (int(x2[-1]) - int(x1[-1]))*12 + index2 - index1

		for j in range(len(list_notes['note'])):
			if len(list_notes['note'][j]) == 0: break
			total += len(list_notes['note'][j])
			for i in range(len(list_notes['note'][j])-1):
				fitness = fitness + distance(list_notes['note'][j][i], list_notes['note'][j][i+1])/list_notes['temps'][j][i]
		return fitness/total


	


	
		
