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
    return sum([value for value in vector])


def update_vector(vector, current, l_rate):
    for i, prob in enumerate(vector):
        vector[i] = prob * (1 - l_rate) + current['bitstring'][i] * l_rate


def mutate_vector(vector, coefficient, rate):
    for i, prob in enumerate(vector):
        if random.random() < rate:
            vector[i] = prob * (1 - coefficient) + \
                random.random() * coefficient


def search(num_bits, max_iter, num_samples, p_mutate, mut_factor, l_rate):
    vector = [0.5 for _ in range(num_bits)]
    best = None
    for _ in range(max_iter):
        current = None
        for _ in range(num_samples):
            candidate = generate_candidate(vector)
            candidate['cost'] = onemax(candidate['bitstring'])
            if current == None or candidate['cost'] > current['cost']:
                current = candidate
            if best == None or candidate['cost'] > best['cost']:
                best = candidate
        update_vector(vector, current, l_rate)
        mutate_vector(vector, mut_factor, p_mutate)
        if best['cost'] == num_bits:
            break
    return best


if __name__ == '__main__':
    num_bits = 64
    max_iter = 100
    num_samples = 100
    p_mutate = 1.0/num_bits
    mut_factor = 0.05
    l_rate = 0.1
    best = search(num_bits, max_iter, num_samples,
                  p_mutate, mut_factor, l_rate)
    print(best['cost'])
