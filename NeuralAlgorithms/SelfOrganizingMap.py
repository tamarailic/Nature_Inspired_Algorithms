import random
import math


def rand_in_bounds(lower_bound, upper_bound):
    return lower_bound + ((upper_bound-lower_bound) * random.random())


def random_vector(search_space):
    return [rand_in_bounds(search_space[i][0], search_space[i][1]) for i in range(len(search_space))]


def euclidean_distance(c1, c2):
    s = 0
    for i in range(len(c1)):
        s += (c1[i]-c2[i])**2.0
    return math.sqrt(s)


def initialize_vectors(domain, width, height):
    codebook_vectors = []
    for x in range(width):
        for y in range(height):
            codebook = {}
            codebook['vector'] = random_vector(domain)
            codebook['coord'] = [x, y]
            codebook_vectors.append(codebook)
    return codebook_vectors


def summarize_vectors(vectors):
    minmax = [[1, 0] for _ in range(len(vectors[0]['vector']))]
    for c in vectors:
        for i, v in enumerate(c['vector']):
            minmax[i][0] = v if v < minmax[i][0] else minmax[i][0]
            minmax[i][1] = v if v > minmax[i][1] else minmax[i][1]
    return minmax


def get_best_matching_unit(codebook_vectors, pattern):
    best, b_dist = None, None
    for codebook in codebook_vectors:
        dist = euclidean_distance(codebook['vector'], pattern)
        if b_dist is None or dist < b_dist:
            best, b_dist = codebook, dist
    return best, b_dist


def update_codebook_vector(bmu, pattern, lrate):
    for i, v in enumerate(bmu['vector']):
        error = pattern[i]-bmu['vector'][i]
        bmu['vector'][i] += lrate * error


def get_vectors_in_neighborhood(bmu, codebook_vectors, neigh_size):
    neighborhood = []
    for other in codebook_vectors:
        if euclidean_distance(bmu['coord'], other['coord']) <= neigh_size:
            neighborhood.append(other)
    return neighborhood


def train_network(vectors, shape, iterations, l_rate, neighborhood_size):
    for iter in range(iterations):
        pattern = random_vector(shape)
        lrate = l_rate * (1.0-(iter/iterations))
        neigh_size = neighborhood_size * (1.0-(iter/iterations))
        bmu, dist = get_best_matching_unit(vectors, pattern)
        neighbors = get_vectors_in_neighborhood(bmu, vectors, neigh_size)
        for node in neighbors:
            update_codebook_vector(node, pattern, lrate)
        print(f">training: neighbors={len(neighbors)}, bmu_dist={dist}")


def test_network(codebook_vectors, shape, num_trials=100):
    error = 0
    for _ in range(num_trials):
        pattern = random_vector(shape)
        bmu, dist = get_best_matching_unit(codebook_vectors, pattern)
        error += dist
    error /= num_trials
    print(f"Finished, average error={error}")
    return error


def execute(domain, shape, iterations, l_rate, neigh_size, width, height):
    vectors = initialize_vectors(domain, width, height)
    summarize_vectors(vectors)
    train_network(vectors, shape, iterations, l_rate, neigh_size)
    test_network(vectors, shape)
    summarize_vectors(vectors)
    return vectors


if __name__ == '__main__':
    domain = [[0.0, 1.0], [0.0, 1.0]]
    shape = [[0.3, 0.6], [0.3, 0.6]]
    iterations = 100
    l_rate = 0.3
    neigh_size = 5
    width, height = 4, 5
    execute(domain, shape, iterations, l_rate, neigh_size, width, height)
