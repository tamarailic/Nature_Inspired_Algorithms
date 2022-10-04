import random


def generate_space(lower_bound, upper_bound):
    space = []
    for _ in range(problem_size):
        space.append([lower_bound, upper_bound])

    return space


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


def init_population():
    population = []
    for _ in range(pop_size):
        member = {}
        member['vector'] = random_vector(search_space)
        population.append(member)

    for member in population:
        member['cost'] = objective_function(member['vector'])

    return population


def create_children(population):
    children = []
    for i in range(pop_size):
        p1, p2, p3 = select_parents(i)
        children.append(de_rand_1_bin(
            population[i], population[p1], population[p2], population[p3]))
    return children


def select_parents(index):
    p1 = random.randint(0, pop_size - 1)
    while p1 == index:
        p1 = random.randint(0, pop_size - 1)
    p2 = random.randint(0, pop_size - 1)
    while p2 == p1 or p2 == index:
        p2 = random.randint(0, pop_size - 1)
    p3 = random.randint(0, pop_size - 1)
    while p3 == p1 or p3 == p2 or p3 == index:
        p3 = random.randint(0, pop_size - 1)
    return p1, p2, p3


def de_rand_1_bin(p0, p1, p2, p3):
    sample = {'vector': [0] * len(p1['vector'])}
    cut = random.randint(0, len(sample['vector']) - 1) + 1
    for i in range(len(sample['vector'])):
        sample['vector'][i] = p0['vector'][i]
        if i == cut or random.random() < crossf:
            v = p3['vector'][i] + weightf * (p1['vector'][i] - p2['vector'][i])
            v = min(search_space[i][1], v)
            v = max(search_space[i][0], v)
            sample['vector'][i] = v

    return sample


def select_population(parents, children):
    population = []
    for i in range(len(parents)):
        if children[i]['cost'] <= parents[i]['cost']:
            population.append(children[i])
        else:
            population.append(parents[i])
    return population


def search():
    population = init_population()
    population = sorted(population, key=lambda x: x['cost'])
    best = population[0]

    for _ in range(max_gens):
        children = create_children(population)
        for child in children:
            child['cost'] = objective_function(child['vector'])
        population = select_population(population, children)
        population = sorted(population, key=lambda x: x['cost'])
        if population[0]['cost'] < best['cost']:
            best = population[0]

    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = generate_space(-5, 5)
    max_gens = 200
    pop_size = 10 * problem_size
    weightf = 0.8
    crossf = 0.9
    best = search()
    print(best)
