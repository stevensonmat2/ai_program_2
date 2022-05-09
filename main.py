"""
Create population of states
each state is a string of queen positions
index is the column, number is the row position fo a queen

find dominate candidates (those with best fitness scores based on fewest attacking queens)
pair off randomly selected states (random chance determined by state_score/sum(total_population_state_score))
generate two child states but slicing parent states and recombining
chance that mutation may also occur in children (modifiy one element of the string)

each iteration, the parent population is replaced by the child population
go until a winning state is found


Population:

select 250 pairs to reproduce
selection is based on fitness, so many individuals can be selected multiple times
pairs always produce new pairs
old population is completely replaced by new population

crossover is a simple split, with crossover chosen randomly

mutation just chnages one cell

needs:

state node

simulation object

fitness: determined by number of non-attacking queens
how to determine number of non attacking queens:

to save time: maybe save coordinate pairs in dictionary to save on computing 

if abs x1- y1 == x2 - y2 OR x1+y1 == x2+y2

simulation has population

simualtion instigates a new generations

simulation randonly selects pairs for mating and adds their offspring to a new population
selects until new population is of correct size

"""

from select import select
import sys
import random
import copy

from boto import GENERATION_RE


if len(sys.argv) > 1:
    POPULATION_SIZE = int(sys.argv[1])
    if len(sys.argv) > 2:
        GENERATION_COUNT = int(sys.argv[2])
else:
    POPULATION_SIZE = 500
    GENERATION_COUNT = 100
MAX_FITNESS = 28


class StateNode:
    def __init__(self, state) -> None:
        self.state_string = state
        self.fitness_score = self.calculate_fitness_score()
        self.mutate()

    def __str__(self) -> str:
        return f"state:{self.state_string}, fitness: {self.fitness_score} "

    def reproduce(self, mate):
        children = []
        crossover_point = random.randint(1,6)

        parent_one_slice = self.state_string[crossover_point:]
        parent_two_slice = mate.state_string[:crossover_point]

        children.append(StateNode(parent_one_slice + parent_two_slice))

        parent_one_slice = self.state_string[:crossover_point]
        parent_two_slice = mate.state_string[crossover_point:]

        children.append(StateNode(parent_two_slice + parent_one_slice))

        return children

    def mutate(self):
        mutate = random.randint(0,99)
        if mutate <= 2:
            new_state = ""
            cell_to_mutate = random.randint(0, 7)
            for index, cell in enumerate(self.state_string):
                if index != cell_to_mutate:
                    new_state = new_state + cell
                else:
                    new_state = new_state + str(random.randint(0, 7))
            self.state_string = new_state


    def calculate_fitness_score(self):
        """
        fitness: determined by number of non-attacking queens
        how to determine number of non attacking queens:
        to save time: maybe save coordinate pairs in dictionary to save on computing
        if abs x1- y1 == x2 - y2 OR x1+y1 == x2+y2
        """
        state = self.state_string
        score = MAX_FITNESS

        for queen_one_x, queen_one_y in enumerate(state[:-1]):
            for queen_two_x, _ in enumerate(state[queen_one_x + 1 :]):
                queen_one = (queen_one_x, int(queen_one_y))
                queen_two = ((queen_one_x+1+queen_two_x), int(state[queen_one_x+1+queen_two_x]))

                if queen_one_y == state[queen_one_x+1+queen_two_x]:
                    score -= 1
                if self.queens_share_diagonals(queen_one, queen_two):
                    score -= 1

        return score

    def queens_share_diagonals(self, queen_one, queen_two):
        q_one_x = queen_one[0]
        q_one_y = queen_one[1]
        q_two_x = queen_two[0]
        q_two_y = queen_two[1]

        if abs(q_one_x - q_two_x) == abs(q_one_y - q_two_y):
            return True

        return False


class Population:
    def __init__(self) -> None:
        pass

class Simulation:
    def __init__(self, population_size=500) -> None:
        self.population_size = population_size
        self.average_fitness = 0
        self.total_fitness = 0
        self.population = self.generate_random_population()

    def generate_random_population(self):
        population = []
        for state in range(1, self.population_size):
            state = "".join([str(random.randint(0, 7)) for x in range(8)])
            population.append(StateNode(state))
            self.total_fitness += population[-1].fitness_score
            population.sort(key=lambda x: x.fitness_score, reverse=True)

        self.average_fitness = self.total_fitness / POPULATION_SIZE
        return population

    def run_simulation(self, generation_count=100):
        while generation_count:
            population = []
            total_fitness = 0

            while len(population) < POPULATION_SIZE:
                pair = self.select_pair()
                population.extend(pair[0].reproduce(pair[1]))
                total_fitness += pair[0].fitness_score + pair[1].fitness_score
                population.sort(key=lambda x: x.fitness_score, reverse=True)
            
                if population[0].fitness_score == MAX_FITNESS:
                    print("found!", population[0])
                    return population[0]

            self.population = copy.deepcopy(population)
            self.total_fitness = total_fitness
            self.average_fitness = total_fitness / POPULATION_SIZE
            print(self.average_fitness)
            generation_count -= 1


    def select_pair(self):
        weights = [self.population[index].fitness_score for index,_ in enumerate(self.population)]
        selected_pair = random.choices(self.population, weights=weights, k=2)

        return selected_pair

node = StateNode("71306425")
print(node)
simulation = Simulation(POPULATION_SIZE)
simulation.run_simulation(GENERATION_COUNT)
# print(simulation.population[0])