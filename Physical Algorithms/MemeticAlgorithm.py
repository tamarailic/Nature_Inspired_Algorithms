import random


def random_bitstring(num_bits):
    bitstring = ''
    for _ in range(num_bits):
        bitstring += '1' if random.random() < 0.5 else '0'
    return bitstring


def decode(bitstring, search_space, bits_per_param):
    vector = []
    for i, bounds in enumerate(search_space):
        off, sum = i * bits_per_param, 0
        param = list(reversed(bitstring[off: off+bits_per_param]))
        for j in range(len(param)):
            sum += (1.0 if (param[j] == '1') else 0.0) * (2.0 ** j)
        min, max = bounds
        vector.append(min + ((max-min)/((2.0**bits_per_param)-1.0)) * sum)
    return vector


def objective_function(vector):
    return sum([x**2 for x in vector])


def fitness(candidate, search_space, param_bits):
    candidate['vector'] = decode(
        candidate['bitstring'], search_space, param_bits)
    candidate['fitness'] = objective_function(candidate['vector'])


def binary_tournament(pop):
    i, j = random.randint(0, len(pop) - 1), random.randint(0, len(pop) - 1)
    while i == j:
        j = random.randint(0, len(pop) - 1)
    return pop[i] if pop[i]['fitness'] < pop[j]['fitness'] else pop[j]


def crossover(parent1, parent2, rate):
    if random.random() >= rate:
        return "" + parent1
    child = ''
    for i in range(len(parent1)):
        child += parent1[i] if random.random() < 0.5 else parent2[i]
    return child


def point_mutation(bitstring, rate=None):
    if rate == None:
        rate = 1.0/len(bitstring)
    child = ""
    for i in range(len(bitstring)):
        bit = bitstring[i]
        if random.random() < rate:
            if bit == '0':
                child += '1'
            else:
                child += '1'
        else:
            child += bit
    return child


def reproduce(selected, pop_size, p_cross, p_mut):
    children = []
    for i, p1 in enumerate(selected):
        p2 = selected[i + 1] if i % 2 == 0 else selected[i - 1]
        if i == len(selected) - 1:
            p2 = selected[0]
        child = {}
        child['bitstring'] = crossover(
            p1['bitstring'], p2['bitstring'], p_cross)
        child['bitstring'] = point_mutation(child['bitstring'], p_mut)
        children.append(child)
    return children


def bitclimber(child, search_space, p_mut, max_local_gens, bits_per_param):
    current = child
    for _ in range(max_local_gens):
        candidate = {}
        candidate['bitstring'] = point_mutation(current['bitstring'], p_mut)
        fitness(candidate, search_space, bits_per_param)
        if candidate['fitness'] <= current['fitness']:
            current = candidate
    return current


def search(max_gens, search_space, pop_size, p_cross, p_mut,
           max_local_gens, p_local, bits_per_param=16):
    pop = [{'bitstring': random_bitstring(
        len(search_space) * bits_per_param)} for i in range(pop_size)]
    for p in pop:
        fitness(p, search_space, bits_per_param)
    best = sorted(pop, key=lambda x: x['fitness'])[0]
    for i in range(max_gens):
        selected = [binary_tournament(pop) for _ in range(pop_size)]
        children = reproduce(selected, pop_size, p_cross, p_mut)
        for child in children:
            fitness(child, search_space, bits_per_param)
        pop = []
        for child in children:
            if random.random() < p_local:
                child = bitclimber(child, search_space, p_mut, max_local_gens,
                                   bits_per_param)
            pop.append(child)
        pop = sorted(pop, key=lambda x: x['fitness'])
        if pop[0]['fitness'] < best['fitness']:
            best = pop[0]
    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 100
    pop_size = 100
    p_cross = 0.98
    p_mut = 1.0/(problem_size*16)
    max_local_gens = 20
    p_local = 0.5
    best = search(max_gens, search_space, pop_size, p_cross, p_mut,
                  max_local_gens, p_local)
    print(best['fitness'])
