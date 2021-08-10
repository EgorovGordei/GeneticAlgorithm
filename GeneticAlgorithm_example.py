from GeneticAlgorithm import *


class SimpleAnimal:
    "Create random unit"
    def __init__(self):
        self.DNA = [random.random() * 10]

    "Return new unit from other 2"
    def propagate(self, other):
        new_animal = SimpleAnimal()
        new_animal.DNA = [(self.DNA[0] + other.DNA[0]) / 2]
        return new_animal

    "Random mutation, return nothing"
    def mutate(self):
        self.DNA[0] += (0.5 - random.random()) ** 3

    def __str__(self):
        return str(self.DNA)


def simple_fitness(populations):
    '''
    Return list of lists of non-negative numbers with non-zero sum
    according to units' fitnesses
    '''
    result = [[max(0.00001, 150 - abs(unit.DNA[0] ** 2 + unit.DNA[0] - 15.25))
                      for unit in population]
                      for population in populations] # solution to x^2+x-15.25
    return result


GA = GeneticAlgorithm(animal_type=SimpleAnimal,
                      population_size=3,
                      fitness_function=simple_fitness,
                      populations_amount=2)
for generation in GA.run(seconds=5*60, fitness_bigger=149.8, keep_amount = 2):
    print("\n\nPop: ", end='')
    for pop in generation[0]:
        print("\n     ", end='')
        for unit in pop:
            print(unit, end=' ')
    print("\nFit: ", end='')
    for fit in generation[1]:
        print("\n    ", fit, end='')
