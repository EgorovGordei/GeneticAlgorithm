import time
import random
import math


def random_weighted(iterable):
        '''
        Random choice of element from iterable
            with probabilities according to elements values
        sum(iterable) must be >= 1
        '''
        value = random.random()
        index = 0
        while value > iterable[index]:
            value -= iterable[index]
            index += 1
        return index

def normalise(iterable):
    "Return same iterable but decreased so sum is 1"
    s = sum(iterable)
    return [(i / s) for i in iterable]


class GeneticAlgorithm:
    '''
    This class provides interface for adapting and evolving
    '''
        
    def __init__(self,
                 animal_type=None,
                 population_size=None,
                 fitness_function=None,
                 populations_amount=1):
        self.animal_type = animal_type
        self.population_size = population_size
        self.fitness_function = fitness_function
        self.populations_amount = populations_amount
        self.populations = []

    def repopulate(self, i):
        self.populations[i] = [self.animal_type()
                               for j in range(self.population_size)]

    def run(self, generations=-1, seconds=10, fitness_bigger=-1,
                keep_amount=5, keep_fitness=0.01):
        '''
        Use this function to start survival:
        generations - amount of generation for algorithm to calculate;
                      use -1 to create infinite loop
        seconds - amount of seconds before shutdown
                  use -1 to create infinite loop
        keep_amount - amount of units kept in each generation
                      if set to -1, keep_fitness is used
        keep_fitness - threshold of fitness needed to survive
                      if set to -1, keep_amount is used
        '''
        start_time = time.time()

        if len(self.populations) == 0:
            self.populations = [None] * self.populations_amount
            for i in range(self.populations_amount):
                self.repopulate(i)
        i = 0
        while i < generations or generations == -1:
            fitnesses = self.fitness_function(self.populations)

            if time.time() - start_time > seconds and seconds != -1:
                return [self.populations, fitnesses]
            else:
                yield [self.populations, fitnesses]

            for j in range(len(fitnesses)):
                fitness = [f for f in fitnesses[j]]
                population = [u for u in self.populations[j]]
                to_sort = [[a, b] for a, b in zip(fitness, population)]
                to_sort.sort(key=lambda pair: -pair[0])
                fitness = [e[0] for e in to_sort]
                population = [e[1] for e in to_sort]

                if fitness_bigger != -1 and fitness[0] >= fitness_bigger:
                    return [self.populations, fitnesses]
            
                fitness = normalise(fitness)
                new_fitness = [f for f in fitness]
                new_population = [u for u in population]
                if keep_amount != -1:
                    new_population = new_population[0:keep_amount]
                    new_fitness = new_fitness[0:keep_amount]
                else:
                    if keep_fitness != -1:
                        while len(new_population) > 0:
                            if new_fitness[-1] < keep_fitness:
                                new_fitness.pop()
                                new_population.pop()
                    else:
                        raise Exception("Nor keep_amount neither keep_fitness was set")

                if len(new_population) == 0:
                    self.repopulate(j)
                    continue
                while len(new_population) < self.population_size:
                    index_1 = random_weighted(fitness)
                    index_2 = random_weighted(fitness)
                    u = population[index_1].propagate(population[index_2])
                    new_population.append(u)

                self.populations[j] = new_population
                for unit in self.populations[j]:
                     unit.mutate()


