# genome: [row_par, pick_par]
# row_par: [random_choice, fullest_row, emptiest_row]
# pick_par: [random_choice, most_sticks, least_sticks]

from random import choice
import random as r
from numpy import random
from Nim import Nim, Nimply

NUMBER_OF_GAMES = 100

class Individual:
    row_random_choice = 1/3
    row_fullest = 1/3
    row_emptiest = 1/3
    pick_random_choice = 1/3
    pick_most_sticks = 1/3
    pick_least_sticks = 1/3
    total_row_p = 1.0
    total_pick_p = 1.0
    fitness = -1
    
    def __init__(self, parameters=None):
        if(parameters is not None):
            self.row_random_choice = parameters[0]
            self.row_fullest = parameters[1]
            self.row_emptiest = parameters[2]
            self.pick_random_choice = parameters[3]
            self.pick_most_sticks = parameters[4]
            self.pick_least_sticks = parameters[5]
            
            self.total_row_p = self.row_random_choice + self.row_fullest + self.row_emptiest
            self.total_pick_p = self.pick_random_choice + self.pick_most_sticks + self.pick_least_sticks

    def __str__(self):
        return f"Genome: {self.row_random_choice}, {self.row_fullest}, {self.row_emptiest}, {self.pick_random_choice}, {self.pick_most_sticks}, {self.pick_least_sticks}, Fitness: {self.fitness}"
    
    def mutate(self, mutation_step=0.001):
        row_random_choice = self.row_random_choice + random.normal(0, mutation_step)
        row_fullest = self.row_fullest + random.normal(0, mutation_step)
        row_emptiest = self.row_emptiest + random.normal(0, mutation_step)
        
        pick_random_choice = self.pick_random_choice + random.normal(0, mutation_step)
        pick_most_sticks = self.pick_most_sticks + random.normal(0, mutation_step)
        pick_least_sticks = self.pick_least_sticks + random.normal(0, mutation_step)
        
        return Individual([row_random_choice, row_fullest, row_emptiest, pick_random_choice, pick_most_sticks, pick_least_sticks])
    
    def recombine(self, other):
        row_random_choice = choice([self.row_random_choice, other.row_random_choice])
        row_fullest = choice([self.row_fullest, other.row_fullest])
        row_emptiest = choice([self.row_emptiest, other.row_emptiest])
        pick_random_choice = choice([self.pick_random_choice, other.pick_random_choice])
        pick_most_sticks = choice([self.pick_most_sticks, other.pick_most_sticks])
        pick_least_sticks = choice([self.pick_least_sticks, other.pick_least_sticks])
        
        return Individual([row_random_choice, row_fullest, row_emptiest, pick_random_choice, pick_most_sticks, pick_least_sticks])
    
    def evaluate(self, training_strategy):
        wins = 0
        for _ in range(NUMBER_OF_GAMES):
            wins += Nim.play([self.strategy, training_strategy])
        self.fitness = wins / NUMBER_OF_GAMES

        
    def strategy(self, state: Nim) -> Nimply: 
        row_selector = random.uniform(0, self.total_row_p)
        available_rows = [i for i in range(len(state.rows)) if state.rows[i] > 0]
        row = int()
        if (row_selector < self.row_random_choice):
            row = choice(available_rows)
        elif (row_selector < self.row_random_choice + self.row_fullest):
            row = state._rows.index(max(state._rows))
        else:
            row = state._rows.index(min([x for x in state._rows if x > 0]))
            
        pick_selector = random.uniform(0, self.total_pick_p)
        if (pick_selector < self.pick_random_choice):
            sticks = r.randint(1, state.rows[row])
        elif (pick_selector < self.pick_random_choice + self.pick_most_sticks):
            sticks = r.randint(1, state.rows[row])
        else:
            sticks = 1
            
        return Nimply(row, sticks)
    