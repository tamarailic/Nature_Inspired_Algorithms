import random


def generate_candidate(vector):
    candidate = {}
    candidate['bitstring'] = [0] * len(vector)
    for i, prob in enumerate(vector):
        if random.random() < prob:
            candidate['bitstring'][i] = 1
        else:
            candidate['bitstring'][i] = 0
    candidate['cost'] = onemax(candidate['bitstring'])
    return candidate


def onemax(vector):
    return sum(vector)


def update_vector(vector, winner, loser, pop_size):
    for i in range(len(vector)):
        if winner['bitstring'][i] != loser['bitstring'][i]:
            if winner['bitstring'][i] == 1:
                vector[i] += 1.0/pop_size
            else:
                vector[i] -= 1.0/pop_size


def search(num_bits, max_iterations, pop_size):
    vector = [0.5 for _ in range(num_bits)]
    best = None
    for _ in range(max_iterations):
        c1 = generate_candidate(vector)
        c2 = generate_candidate(vector)
        if c1['cost'] > c2['cost']:
            winner, loser = c1, c2
        else:
            winner, loser = c2, c1
        if best == None or winner['cost'] > best['cost']:
            best = winner
        update_vector(vector, winner, loser, pop_size)
        if best['cost'] == num_bits:
            break
    return best


if __name__ == '__main__':
    num_bits = 32
    max_iter = 200
    pop_size = 20
    best = search(num_bits, max_iter, pop_size)
    print(best['cost'])
