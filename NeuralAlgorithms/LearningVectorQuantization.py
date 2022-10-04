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


def generate_random_pattern(domain):
    class_label = list(domain.keys())[
        random.randint(0, len(domain.keys()) - 1)]
    pattern = {'label': class_label}
    pattern['vector'] = random_vector(domain[class_label])
    return pattern


def initialize_vectors(domain, num_vectors):
    codebook_vectors = []
    for _ in range(num_vectors):
        selected_class = list(domain.keys())[
            random.randint(0, len(domain.keys()) - 1)]
        codebook = {}
        codebook['label'] = selected_class
        codebook['vector'] = random_vector([[0, 1], [0, 1]])
        codebook_vectors.append(codebook)
    return codebook_vectors


def get_best_matching_unit(codebook_vectors, pattern):
    best, b_dist = None, None
    for codebook in codebook_vectors:
        dist = euclidean_distance(codebook['vector'], pattern['vector'])
        if b_dist is None or dist < b_dist:
            best, b_dist = codebook, dist
    return best


def update_codebook_vector(bmu, pattern, lrate):
    for i, v in enumerate(bmu['vector']):
        error = pattern['vector'][i]-bmu['vector'][i]
        if bmu['label'] == pattern['label']:
            bmu['vector'][i] += lrate * error
        else:
            bmu['vector'][i] -= lrate * error


def train_network(codebook_vectors, domain, iterations, learning_rate):
    for iter in range(iterations):
        pat = generate_random_pattern(domain)
        bmu = get_best_matching_unit(codebook_vectors, pat)
        lrate = learning_rate * (1.0-(iter/iterations))
        if iter % 10 == 0:
            print("> iter={iter}, got={bmu['label']}, exp={pat['label']}")
        update_codebook_vector(bmu, pat, lrate)


def test_network(codebook_vectors, domain, num_trials=100):
    correct = 0
    for _ in range(num_trials):
        pattern = generate_random_pattern(domain)
        bmu = get_best_matching_unit(codebook_vectors, pattern)
        if bmu['label'] == pattern['label']:
            correct += 1
    print(f"Done. Score: {correct}/{num_trials}")
    return correct


def execute(domain, iterations, num_vectors, learning_rate):
    codebook_vectors = initialize_vectors(domain, num_vectors)
    train_network(codebook_vectors, domain, iterations, learning_rate)
    test_network(codebook_vectors, domain)
    return codebook_vectors


if __name__ == '__main__':
    domain = {"A": [[0, 0.4999999], [0, 0.4999999]], "B": [[0.5, 1], [0.5, 1]]}
    learning_rate = 0.3
    iterations = 1000
    num_vectors = 20
    execute(domain, iterations, num_vectors, learning_rate)
