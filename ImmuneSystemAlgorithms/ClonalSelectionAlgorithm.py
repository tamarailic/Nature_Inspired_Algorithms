import random
import math


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
            if param[j] == '1':
                sum += 1 * (2.0 ** j)
        min, max = bounds
        vector.append(min + ((max-min)/((2.0**bits_per_param)-1.0)) * sum)
    return vector


def evaluate(candidates, search_space, param_bits):
    for candidate in candidates:
        candidate['vector'] = decode(
            candidate['bitstring'], search_space, param_bits)
        candidate['cost'] = objective_function(candidate['vector'])


def objective_function(bitstring):
    return sum([v**2 for v in bitstring])


def point_mutation(bitstring, rate):
    mutated_child = ''

    for i in range(len(bitstring)):
        random_chance = random.random()
        if random_chance < rate:
            if bitstring[i] == '1':
                mutated_child += '0'
            else:
                mutated_child += '1'
        else:
            mutated_child += bitstring[i]
    return mutated_child


def num_clones(pop_size, clone_factor):
    return math.floor(pop_size * clone_factor)


def calculate_affinity(pop):
    pop = sorted(pop, key=lambda x: x['cost'])
    range = pop[-1]['cost'] - pop[0]['cost']
    if range == 0:
        for p in pop:
            p['affinity'] = 1
    else:
        for p in pop:
            p['affinity'] = 1 - (p['cost']/range)


def calculate_mutation_rate(antibody, mutate_factor=-2.5):
    return math.exp(mutate_factor * antibody['affinity'])


def clone_and_hypermutate(pop, clone_factor):
    clones = []
    n_clones = num_clones(len(pop), clone_factor)
    calculate_affinity(pop)
    for antibody in pop:
        m_rate = calculate_mutation_rate(antibody)
        for _ in range(n_clones):
            clone = {}
            clone['bitstring'] = point_mutation(antibody['bitstring'], m_rate)
            clones.append(clone)
    return clones


def random_insertion(search_space, pop, num_rand, bits_per_param):
    if num_rand == 0:
        return pop
    rands = [{'bitstring': random_bitstring(
        len(search_space) * bits_per_param)} for _ in range(num_rand)]
    evaluate(rands, search_space, bits_per_param)
    return sorted(pop + rands, key=lambda x: x['cost'])[:len(pop)]


def search(search_space, max_gens, pop_size, clone_factor, num_rand,
           bits_per_param=16):
    pop = [{'bitstring': random_bitstring(
        len(search_space) * bits_per_param)} for _ in range(pop_size)]
    evaluate(pop, search_space, bits_per_param)
    best = min(pop, key=lambda x: x['cost'])
    for _ in range(max_gens):
        clones = clone_and_hypermutate(pop, clone_factor)
        evaluate(clones, search_space, bits_per_param)
        pop = sorted(pop + clones, key=lambda x: x['cost'])[:pop_size]
        pop = random_insertion(search_space, pop, num_rand, bits_per_param)
        best = min(pop + [best], key=lambda x: x['cost'])
    return best


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 100
    pop_size = 100
    clone_factor = 0.1
    num_rand = 2
    best = search(search_space, max_gens, pop_size, clone_factor, num_rand)
    print(best['cost'], best['vector'])
