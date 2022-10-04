import random
import math


def generate_space(lower_bound, upper_bound):
    space = []
    for _ in range(problem_size):
        space.append([lower_bound, upper_bound])

    return space


def init_population():
    strategy = []
    population = []
    for i in range(problem_size):
        strategy.append([0, (search_space[i][1] - search_space[i][0]) * 0.02])

    for _ in range(pop_size):
        member = {}
        member['vector'] = random_vector(search_space)
        member['strategy'] = random_vector(strategy)
        population.append(member)

    for member in population:
        member['fitness'] = objective_function(member['vector'])

    return population


def random_vector(space):
    vector = []

    for i in range(len(search_space)):
        vector.append(space[i][0] + (space[i][1] -
                      space[i][0]) * random.random())

    return vector


def objective_function(vector):
    sum = 0
    for v in vector:
        sum += v ** 2

    return sum


def mutate(member):
    child = {}
    child['vector'] = mutate_problem(member['vector'], member['strategy'])
    child['strategy'] = mutate_strategy(member['strategy'])
    return child


def mutate_problem(vector, strategy):
    child = []
    for i in range(len(vector)):
        state = vector[i] + strategy[i] * random_gaussian()
        if state < search_space[i][0]:
            child.append(search_space[i][0])
        elif state > search_space[i][1]:
            child.append(search_space[i][1])
        else:
            child.append(state)
    return child


def mutate_strategy(strategy):
    tau = math.sqrt(2 * len(strategy)) ** (-1)
    tau_p = math.sqrt(2 * math.sqrt(len(strategy))) ** (-1)
    child_strategy = []
    for i in range(len(strategy)):
        child_strategy.append(
            strategy[i] * math.exp(tau_p * random_gaussian() + tau * random_gaussian()))

    return child_strategy


def random_gaussian(mean=0, stdev=1):
    u1, u2, w = 0, 0, 0
    while True:
        u1 = 2 * random.random() - 1
        u2 = 2 * random.random() - 1
        w = u1 * u1 + u2 * u2
        if w < 1:
            break
    w = math.sqrt((-2 * math.log(w)) / w)
    return mean + (u2 * w) * stdev


def search():
    population = init_population()
    population = sorted(population, key=lambda x: x['fitness'])
    best = population[0]
    for _ in range(max_gens):
        children = []
        for i in range(num_children):
            children.append(mutate(population[i]))

        for child in children:
            child['fitness'] = objective_function(child['vector'])
        union = []
        union += children
        union += population
        union = sorted(union, key=lambda x: x['fitness'])
        union_best = union[0]
        if union_best['fitness'] < best['fitness']:
            best = union[0]
        population = union[:pop_size]

    return best


if __name__ == '__main__':
    problem_size = 2
    pop_size = 30
    search_space = generate_space(-5, 5)
    max_gens = 100
    num_children = 20
    best = search()
    print(best['fitness'])
