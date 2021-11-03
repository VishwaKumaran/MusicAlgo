# ==============================================================================
"""Creer un algorithme génétique permettant de générer un morceau"""
# ==============================================================================
__author__  = "COULIBALY Papa Garba, DECULTOT Gauthier, ELANKUMARAN Vishwa"
__version__ = "2.0"
__date__    = "2020-03-10"
# ==============================================================================
from music21 import *
import numpy
from fractions import Fraction
# ------------------------------------------------------------------------------
class Genetique(object):
	"""Algorithme Genetique"""
	def __init__(self):
		self.tx_mutation = 0.01
		self.tx_high_select = 0.1  
		self.tx_low_select = 0.05
		self.pop = 50
		self.high_select = int(self.pop*self.tx_high_select)  
		self.len_mesure = 4
		self.max_fitness = 0.16
		self.__notes = []
		self.__temps = [Fraction(1/(2**i)) for i in range(-2,3)]
		self.morceau = stream.Stream()
		
		for i in range(4,5):
			for j in 'C#D#EF#G#A#B':
				if j == '#': self.__notes.append(str(self.__notes[-1][0])+str(j)+str(i))
				else: self.__notes.append(str(j)+str(i))
		self.__notes.append("C6")
		

	def get_random_note(self): return numpy.random.choice(self.__notes)

	def get_random_temps(self, temps_actu):
		new_list = [] 
		for element in self.__temps:
			if element+temps_actu <= self.len_mesure: new_list.append(element)
		if len(new_list) == 0: return 0
		return numpy.random.choice(new_list)

	def get_random_individual(self):
		dicto = {} ; liste_note = [] ; liste_temps = [] ; actuel = 0
		while actuel < self.len_mesure:
			liste_note.append(self.get_random_note()) ; liste_temps.append(self.get_random_temps(actuel))
			actuel += liste_temps[-1]
		dicto['note'] = liste_note ; dicto['temps'] = liste_temps
		return dicto

	def get_random_population(self): return [self.get_random_individual() for i in range(self.pop)]

	def get_individual_fitness(self, individu):
		fitness = 0 
		def distance(x1, x2):
			list_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
			index1 = list_notes.index(x1[:2]) if len(x1) == 3 else list_notes.index(x1[0])
			index2 = list_notes.index(x2[:2]) if len(x2) == 3 else list_notes.index(x2[0])
			return (int(x2[-1]) - int(x1[-1]))*12 + index2 - index1

		for i in range(len(individu['note'])-1):
			fitness = fitness + distance(individu['note'][i], individu['note'][i+1])/individu['temps'][i]
		return fitness/len(individu['note'])

	def get_individual_fitness_another(self, individu):
		fitness = 0
		def dissonance(x1, x2):
			list_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] ; dissonant = [1, 2, 3, 5, 7, 10, 11] 
			index1 = list_notes.index(x1[:2]) if len(x1) == 3 else list_notes.index(x1[0])
			index2 = list_notes.index(x2[:2]) if len(x2) == 3 else list_notes.index(x2[0])
			diff_octave = abs(int(x1[-1]) - int(x2[-1]))
			if diff_octave != 0: index2 += 12*diff_octave			
			return 0 if abs(index2-index1) in dissonant else 1

		for i in range(len(individu['note'])-1): fitness = fitness + dissonance(individu['note'][i], individu['note'][i+1])
		return fitness/len(individu['note'])


	def grade_population(self, population):
		grade = [] ; grade_sorted = []
		for individu in population: 
			grade.append((individu, self.get_individual_fitness(individu), abs(self.max_fitness-self.get_individual_fitness(individu)), self.get_individual_fitness_another(individu)))
		first_sort = sorted(grade, key= lambda x: x[3], reverse=True)
		return sorted(first_sort, key= lambda x: x[2])
		#return first_sort

	def average_population(self, population):
		i = 0
		for individu in population: i += self.get_individual_fitness(individu)
		return i/self.pop

	def evolve_population(self, population):
		def mutation(individu):
			choix_pos = numpy.random.choice(len(individu['note']))
			return 'note', choix_pos, self.get_random_note()

		def reproduction(mother, father):					
			temps_actu = 0 ; temps_both = {'mother': sorted(mother['temps'], reverse=True), 'father': sorted(father['temps'], reverse=True) } ; new_baby = {'note': [], 'temps': []}
			while temps_actu < self.len_mesure:
				if len(temps_both['mother']) != 0 and len(temps_both['father']) == 0: choix = 'mother'
				elif len(temps_both['mother']) == 0 and len(temps_both['father']) != 0: choix = 'father'
				else: choix = numpy.random.choice(['mother', 'father']) 
				choix_temps = numpy.random.choice(temps_both[choix])
				new_baby['temps'].append(choix_temps)  
				new_baby['note'].append(mother['note'][mother['temps'].index(choix_temps)] if choix == 'mother' else father['note'][father['temps'].index(choix_temps)])
				
				temps_actu += choix_temps
				for temps_mother in temps_both['mother']:
					if temps_mother+temps_actu <= self.len_mesure: break
					else: temps_both['mother'].remove(temps_mother)
				for temps_father in temps_both['father']:
					if temps_father+temps_actu <= self.len_mesure: break
					else: temps_both['father'].remove(temps_father)
			return new_baby

		grade_pop = self.grade_population(population) ; average = 0 ; grade = [] ; solution = []
		for individu, fitness, distance, dissonance in grade_pop:
			average += fitness ; grade.append(individu)
			# if fitness == self.max_fitness:
			# 	solution.append(individu)
			# 	return population, average, solution
		average /= self.pop 


		parents = grade[:self.high_select]
		
		for individu in grade[self.high_select:]:
			if numpy.random.random() < self.tx_low_select: parents.append(individu)

		for individu in parents:
			if numpy.random.random() < self.tx_mutation:
				mutation_result = mutation(individu) ; individu[mutation_result[0]][mutation_result[1]] = mutation_result[2]

		len_cross = self.pop - len(parents) ; children = []
		while len(children) < len_cross:
		  	mother = numpy.random.choice(parents) ; father = numpy.random.choice(parents)
		  	if mother != father: 
		  		baby = reproduction(mother, father)
		  		children.append(baby)

		return parents + children, average, solution

	def loop(self, population):
		for i in range(len(population)):
			mesure = stream.Stream(); mesure = stream.Measure(number=i+1)
			for j in range(len(population[i]['note'])):
				_note = note.Note(population[i]['note'][j]) ; _note.duration.quarterLength = population[i]['temps'][j]
				mesure.append(_note)
			self.morceau.insert(mesure)
		self.morceau.show()


if __name__ == '__main__':
	a = Genetique()
	population = a.get_random_population()
	average = a.average_population(population)
	print('Starting grade: %.2f' % average, '/ %.2f' % a.max_fitness)

	generation_actu = 0 ; solution = None ; list_aver = []
	while generation_actu < 30:

		population, average, solution = a.evolve_population(population)
		list_aver.append(average)
		generation_actu += 1


	import pygal
	line_chart = pygal.Line(show_dots=False, show_legend=False)
	line_chart.title = 'Fitness evolution'
	line_chart.x_title = 'Generations'
	line_chart.y_title = 'Fitness'
	line_chart.add('Fitness', list_aver)
	line_chart.render_to_file('fitness_evolution.svg')

	print('Final grade: %.2f' % a.average_population(population), '/ %.2f' % (a.max_fitness))
	
	a.loop(population)

	_ = input('Seconde simulation : <Press any key>')

	a = Genetique()
	average = a.average_population(population)
	population = None ; population = a.get_random_population()
	print('Starting grade: %.2f' % average, '/ %.2f' % a.max_fitness)

	generation_actu = 0 ; solution = None ; list_aver = [] ; true_pop = []
	for i in range(30):
		population = None ; population = a.get_random_population()
		while generation_actu < 30:
			population, average, solution = a.evolve_population(population)
			#list_aver.append(average)
			generation_actu += 1
		true_pop.append(population[0])


	# line_chart = pygal.Line(show_dots=False, show_legend=False)
	# line_chart.title = 'Fitness evolution'
	# line_chart.x_title = 'Generations'
	# line_chart.y_title = 'Fitness'
	# line_chart.add('Fitness', list_aver)
	# line_chart.render_to_file('fitness_evolution2.svg')

	print('Final grade: %.2f' % a.average_population(population), '/ %.2f' % a.max_fitness)
	
	a.loop(true_pop)
