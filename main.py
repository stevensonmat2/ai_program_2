import sys
import random
import copy


if len(sys.argv) > 1:
    POPULATION_SIZE = int(sys.argv[1])
    if len(sys.argv) > 2:
        GENERATION_COUNT = int(sys.argv[2])
else:
    POPULATION_SIZE = 500
    GENERATION_COUNT = 1000

MAX_FITNESS = 28


class StateNode:
    def __init__(self, state) -> None:
        self.state_string = state
        self.fitness_score = self.calculate_fitness_score()
        self.check_for_mutation()

    def __str__(self) -> str:
        return f"state:{self.state_string}, fitness: {self.fitness_score} "

    def reproduce(self, mate):
        children = []
        crossover_point = random.randint(1, 6)

        parent_one_slice_one = self.state_string[crossover_point:]
        parent_one_slice_two = self.state_string[:crossover_point]
        parent_two_slice_one = mate.state_string[crossover_point:]
        parent_two_slice_two = mate.state_string[:crossover_point]

        children = [
            StateNode(parent_one_slice_one + parent_two_slice_two),
            StateNode(parent_two_slice_one + parent_one_slice_two),
        ]

        # for i in children:
        #     print(i)

        return children

    def check_for_mutation(self):
        mutate = random.randint(0, 99)
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
        state = self.state_string
        score = MAX_FITNESS

        for queen_one_x, queen_one_y in enumerate(state[:-1]):
            for queen_two_x_offset, _ in enumerate(state[queen_one_x + 1 :]):
                queen_two_x = queen_one_x + queen_two_x_offset + 1
                queen_two_y = state[queen_two_x]
                queen_one = (queen_one_x, int(queen_one_y))
                queen_two = (queen_two_x, int(queen_two_y))

                if queen_one_y == queen_two_y:
                    score -= 1
                elif self.queens_share_diagonals(queen_one, queen_two):
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

        self.average_fitness = self.total_fitness / self.population_size
        return population

    def run_simulation(self, generation_count=100):
        while generation_count:
            population = []
            total_fitness = 0

            while len(population) < self.population_size:
                pair = self.select_pair()
                population.extend(pair[0].reproduce(pair[1]))
                total_fitness += pair[0].fitness_score + pair[1].fitness_score
                population.sort(key=lambda x: x.fitness_score, reverse=True)

                if population[0].fitness_score == MAX_FITNESS:
                    print(
                        f"gen={GENERATION_COUNT - generation_count} found! {population[0]}"
                    )
                    return population[0]

            self.population = copy.deepcopy(population)
            self.total_fitness = total_fitness
            self.average_fitness = self.total_fitness / self.population_size
            print(self.average_fitness)
            generation_count -= 1

    def select_pair(self):
        weights = [
            (self.population[index].fitness_score / MAX_FITNESS)
            for index, _ in enumerate(self.population)
        ]
        selected_pair = random.choices(self.population, weights=weights, k=2)

        return selected_pair

simulation = Simulation(POPULATION_SIZE)
simulation.run_simulation(GENERATION_COUNT)
