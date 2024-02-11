# Description: Evolutionary Strategy (ES) agent for the game of Nim
from random import choice
import random as r
from numpy import random
from datetime import datetime, date
from Nim import Nim, Nimply
from Individual import Individual
from tqdm.auto import tqdm



def selection(population: list()) -> Individual:
    best_individual = Individual()
    for individual in population:
        if individual.fitness > best_individual.fitness:
            best_individual = individual
    return best_individual

def train(training_strategy, population_size=10, max_generations=1000, recombination_probability=0.01, big_mutation_probability=0.1):
    parent = Individual()
    parent.evaluate(training_strategy)
    with tqdm(total=max_generations) as pbar:
        for _ in range(max_generations):
            population = list()
            for _ in range(population_size):
                if random.rand() < big_mutation_probability: child = parent.mutate(0.01)
                else: child = parent.mutate()
                if random.rand() < recombination_probability:
                    child = parent.recombine(child)
                child.evaluate(training_strategy)
                population.append(child)
            pbar.update(1)
            
            parent = selection(population)
    
    print(parent)
    
    
    save_parameters(parent)
    
def es_agent(state: Nim) -> Nimply:
        genome = [0.4484343943223173, 0.2686308016730368, 0.5012035376513981, 0.36669803245027227, 0.3004695157481375, 0.40312900306012334]
        row_selector = random.uniform(0, genome[0] + genome[1] + genome[2])
        available_rows = [i for i in range(len(state.rows)) if state.rows[i] > 0]
        row = int()
        if (row_selector < genome[0]):
            row = choice(available_rows)
        elif (row_selector < genome[0] + genome[1]):
            row = state._rows.index(max(state._rows))
        else:
            row = state._rows.index(min([x for x in state._rows if x > 0]))
            
        pick_selector = random.uniform(0, genome[3] + genome[4] + genome[5])
        if (pick_selector < genome[3]):
            sticks = r.randint(1, state.rows[row])
        elif (pick_selector < genome[3] + genome[5]):
            sticks = r.randint(1, state.rows[row])
        else:
            sticks = 1
            
        return Nimply(row, sticks)

# --------UTILITY FUNCTIONS--------
def save_parameters(parameters):
    today = f'{datetime.now().year}_{datetime.now().month}_{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}_{datetime.now().second}'
    filename = f'ES_agent_parameters_{today}.txt'
    f = open(filename, 'w')
    f.write(f'{parameters.row_random_choice}, {parameters.row_fullest}, {parameters.row_emptiest}, {parameters.pick_random_choice}, {parameters.pick_most_sticks}, {parameters.pick_least_sticks}`\n{parameters.fitness}')
    f.close()

def import_parameters(filename):
    pass