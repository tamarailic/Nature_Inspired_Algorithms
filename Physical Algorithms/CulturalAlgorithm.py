import random


def rand_in_bounds(lower_bound, upper_bound):
    return lower_bound + ((upper_bound-lower_bound) * random.random())


def random_vector(search_space):
    return [rand_in_bounds(search_space[i][0], search_space[i][1]) for i in range(len(search_space))]


def objective_function(vector):
    return sum([x**2 for x in vector])


def initialize_beliefspace(search_space):
    belief_space = {}
    belief_space['situational'] = None
    belief_space['normative'] = [search_space[i]
                                 for i in range(len(search_space))]
    return belief_space


def update_beliefspace_situational(belief_space, best):
    curr_best = belief_space['situational']
    if curr_best == None or best['fitness'] < curr_best['fitness']:
        belief_space['situational'] = best


def mutate_with_int(candidate, beliefs, search_space):
    v = [0] * len(candidate['vector'])
    for i, _ in enumerate(candidate['vector']):
        v[i] = rand_in_bounds(beliefs['normative'][i][0],
                              beliefs['normative'][i][1])
        v[i] = min(search_space[i][1], v[i])
        v[i] = max(search_space[i][0], v[i])
    return {'vector': v}


def binary_tournament(pop):
    i, j = random.randint(0, len(pop) - 1), random.randint(0, len(pop) - 1)
    while i == j:
        j = random.randint(0, len(pop) - 1)
    return pop[i] if pop[i]['fitness'] < pop[j]['fitness'] else pop[j]


def update_beliefspace_normative(belief_space, accepted):
    for i, bounds in enumerate(belief_space['normative']):
        bounds[0] = min(accepted, key=lambda x: x['vector'][i])['vector'][i]
        bounds[1] = max(accepted, key=lambda x: x['vector'][i])['vector'][i]


def search(max_gens, search_space, pop_size, num_accepted):
    pop = [{'vector': random_vector(search_space)} for _ in range(pop_size)]
    belief_space = initialize_beliefspace(search_space)
    for p in pop:
        p['fitness'] = objective_function(p['vector'])
    best = sorted(pop, key=lambda x: x['fitness'])[0]
    update_beliefspace_situational(belief_space, best)
    for _ in range(max_gens):
        children = [mutate_with_int(
            pop[i], belief_space, search_space) for i in range(pop_size)]
        for child in children:
            child['fitness'] = objective_function(child['vector'])
        best = sorted(children, key=lambda x: x['fitness'])[0]
        update_beliefspace_situational(belief_space, best)
        pop = [binary_tournament(children + pop) for _ in range(pop_size)]
        pop = sorted(pop, key=lambda x: x['fitness'])
        accepted = pop[:num_accepted]
        update_beliefspace_normative(belief_space, accepted)
    return belief_space['situational']


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 200
    pop_size = 100
    num_accepted = round(pop_size*0.20)
    best = search(max_gens, search_space, pop_size, num_accepted)
    print(best['fitness'])
