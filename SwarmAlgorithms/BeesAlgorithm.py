import random


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def objective_function(vector):
    return sum([v**2 for v in vector])


def create_neigh_bee(site, patch_size, search_space):
    vector = []
    for i, v in enumerate(site):
        v = v+random.random()*patch_size if random.random() < 0.5 else v - \
            random.random()*patch_size
        v = min(search_space[i][1], v)
        v = max(search_space[i][0], v)
        vector.append(v)
    bee = {}
    bee['vector'] = vector
    return bee


def search_neigh(parent, neigh_size, patch_size, search_space):
    neigh = []
    for _ in range(neigh_size):
        neigh.append(create_neigh_bee(
            parent['vector'], patch_size, search_space))
    for bee in neigh:
        bee['fitness'] = objective_function(bee['vector'])
    return sorted(neigh, key=lambda x: x['fitness'])[0]


def create_scout_bees(search_space, num_scouts):
    return [{'vector': random_vector(search_space)} for _ in range(num_scouts)]


def search(max_gens, search_space, num_bees, num_sites, elite_sites,
           patch_size, e_bees, o_bees):
    best = None
    pop = [{'vector': random_vector(search_space)}]
    for _ in range(max_gens):
        for p in pop:
            p['fitness'] = objective_function(p['vector'])
        pop = sorted(pop, key=lambda x: x['fitness'])
        if best is None or pop[0]['fitness'] < best['fitness']:
            best = pop[0]
        next_gen = []
        for i, parent in enumerate(pop[:num_sites]):
            neigh_size = e_bees if i < elite_sites else o_bees
            next_gen.append(search_neigh(
                parent, neigh_size, patch_size, search_space))
        scouts = create_scout_bees(search_space, (num_bees-num_sites))
        pop = next_gen + scouts
        patch_size = patch_size * 0.95
    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 500
    num_bees = 45
    num_sites = 3
    elite_sites = 1
    patch_size = 3.0
    e_bees = 7
    o_bees = 2
    best = search(max_gens, search_space, num_bees, num_sites, elite_sites,
                  patch_size, e_bees, o_bees)
    print(best['fitness'])
