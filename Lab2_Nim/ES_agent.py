# Description: Evolutionary Strategy (ES) agent for the game of Nim
from numpy import random
from random import choice
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

def train(training_strategy, population_size=10, max_generations=1000, recombination_probability=0.01):
    parent = Individual()
    parent.evaluate(training_strategy)
    with tqdm(total=max_generations) as pbar:
        for _ in range(max_generations):
            population = list()
            for _ in range(population_size):
                if random.rand() < 0.1: child = parent.mutate(0.1)
                else: child = parent.mutate()
                if random.rand() < recombination_probability:
                    child = parent.recombine(child)
                child.evaluate(training_strategy)
                population.append(child)
            pbar.update(1)
            
            parent = selection(population)
    
    print(parent)
    
    
    save_parameters(parent)

# --------UTILITY FUNCTIONS--------
def save_parameters(parameters):
    today = f'{datetime.now().year}_{datetime.now().month}_{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}_{datetime.now().second}'
    filename = f'Lab2_Nim/ES_train/ES_agent_parameters_{today}.txt'
    f = open(filename, 'w')
    f.write(f'{parameters.row_random_choice}, {parameters.row_fullest}, {parameters.row_emptiest}, {parameters.pick_random_choice}, {parameters.pick_most_sticks}, {parameters.pick_least_sticks}`\n{parameters.fitness}')
    f.close()

def import_parameters(filename):
    f = open(filename, 'r')
    parameters = f.read()
    f.close()
    return parameters