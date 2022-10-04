import random


def generate_candidate(vector):
    candidate = {}
    candidate['bitstring'] = [0] * len(vector)
    for i, prob in enumerate(vector):
        if random.random() < prob:
            candidate['bitstring'][i] = 1
        else:
            candidate['bitstring'][i] = 0
    return candidate


def onemax(vector):
    return sum(vector)


def random_bitstring(num_bits):
    bitstring = []
    for _ in range(num_bits):
        if random.random() < 0.5:
            bitstring.append(1)
        else:
            bitstring.append(0)
    return bitstring


def binary_tournament(pop):
    i, j = random.randint(0, len(pop) - 1), random.randint(0, len(pop) - 1)
    while j == i:
        j = random.randint(0, len(pop) - 1)
    if pop[i]['fitness'] > pop[j]['fitness']:
        return pop[i]
    return pop[j]


def calculate_bit_probabilities(pop):
    vector = [0] * len(pop[0]['bitstring'])
    for member in pop:
        for i, bit in enumerate(member['bitstring']):
            vector[i] += bit
    for i, f in enumerate(vector):
        vector[i] = f/len(pop)
    return vector


def search(num_bits, max_iter, pop_size, select_size):
    pop = [{'bitstring': random_bitstring(num_bits)} for _ in range(pop_size)]
    for p in pop:
        p['fitness'] = onemax(p['bitstring'])
    best = sorted(pop, key=lambda x: x['fitness'], reverse=True)[0]
    for _ in range(max_iter):
        selected = [binary_tournament(pop) for _ in range(select_size)]
        vector = calculate_bit_probabilities(selected)
        samples = [generate_candidate(vector) for _ in range(pop_size)]
        for s in samples:
            s['fitness'] = onemax(s['bitstring'])
        samples = sorted(samples, key=lambda x: x['fitness'], reverse=True)
        if samples[0]['fitness'] > best['fitness']:
            best = samples[0]
        pop = samples
    return best


if __name__ == '__main__':
    num_bits = 64
    max_iter = 100
    pop_size = 50
    select_size = 30
    best = search(num_bits, max_iter, pop_size, select_size)
    print(best['fitness'])
