import random
import math


def rand_in_bounds(lower_bound, upper_bound):
    return lower_bound + ((upper_bound-lower_bound) * random.random())


def random_vector(search_space):
    return [rand_in_bounds(search_space[i][0], search_space[i][1]) for i in range(len(search_space))]


def objective_function(vector):
    return sum([x**2 for x in vector])


def distance(c1, c2):
    s = 0
    for i in range(len(c1)):
        s += (c1[i]-c2[i])**2.0
    return math.sqrt(s)


def calculate_normalized_cost(pop):
    pop = sorted(pop, key=lambda x: x['cost'])
    range = pop[-1]['cost'] - pop[0]['cost']
    if range == 0:
        for p in pop:
            p['norm_cost'] = 1
    else:
        for p in pop:
            p['norm_cost'] = 1.0-(p['cost']/range)


def average_cost(pop):
    s = sum([x['cost'] for x in pop])
    return s/len(pop)


def mutation_rate(beta, normalized_cost):
    return (1.0/beta) * math.exp(-normalized_cost)


def random_gaussian(mean=0.0, stdev=1.0):
    u1 = u2 = w = 0
    while True:
        u1 = 2 * random.random() - 1
        u2 = 2 * random.random() - 1
        w = u1 * u1 + u2 * u2
        if w < 1:
            break
    w = math.sqrt((-2.0 * math.log(w)) / w)
    return mean + (u2 * w) * stdev


def mutate(beta, child, normalized_cost):
    for i, v in enumerate(child['vector']):
        alpha = mutation_rate(beta, normalized_cost)
        child['vector'][i] = v + alpha * random_gaussian()


def clone(parent):
    v = [parent['vector'][i] for i in range(len(parent['vector']))]
    return {'vector': v}


def clone_cell(beta, num_clones, parent):
    clones = [clone(parent) for i in range(num_clones)]
    for c in clones:
        mutate(beta, c, parent['norm_cost'])
    for c in clones:
        c['cost'] = objective_function(c['vector'])
    clones = sorted(clones, key=lambda x: x['cost'])
    return clones[0]


def get_neighborhood(cell, pop, aff_thresh):
    neighbours = []
    for p in pop:
        if distance(p['vector'], cell['vector']) < aff_thresh:
            neighbours.append(p)
    return neighbours


def affinity_supress(population, aff_thresh):
    pop = []
    for cell in population:
        neighbors = get_neighborhood(cell, population, aff_thresh)
        neighbors = sorted(neighbors, key=lambda x: x['cost'])
        if neighbors == [] or cell['vector'] == neighbors[0]['vector']:
            pop.append(cell)
    return pop


def search(search_space, max_gens, pop_size, num_clones, beta, num_rand,
           aff_thresh):
    pop = [{'vector': random_vector(
        search_space)} for _ in range(pop_size)]
    best = None
    for k in range(max_gens):
        for p in pop:
            p['cost'] = objective_function(p['vector'])
        calculate_normalized_cost(pop)
        pop = sorted(pop, key=lambda x: x['cost'])
        if best is None or pop[0]['cost'] < best['cost']:
            best = pop[0]
        avgCost, progeny = average_cost(pop), None
        while True:
            progeny = [clone_cell(beta, num_clones, pop[i])
                       for i in range(len(pop))]
            if average_cost(progeny) < avgCost:
                break
        pop = affinity_supress(progeny, aff_thresh)
        for _ in range(num_rand):
            pop.append({'vector': random_vector(search_space)})
    return best


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 150
    pop_size = 20
    num_clones = 10
    beta = 100
    num_rand = 2
    aff_thresh = (search_space[0][1]-search_space[0][0])*0.05
    best = search(search_space, max_gens, pop_size, num_clones, beta,
                  num_rand, aff_thresh)
    print(f"done! Solution: f={best['cost']}, s={best['vector']}")
