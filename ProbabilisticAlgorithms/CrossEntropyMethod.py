import random
import math


def objective_function(vector):
    return sum([x ** 2.0 for x in vector])


def random_variable(minmax):
    min, max = minmax
    return min + ((max - min) * random.random())


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


def generate_sample(search_space, means, stdevs):
    vector = [0] * len(search_space)
    for i in range(len(search_space)):
        vector[i] = random_gaussian(means[i], stdevs[i])
        vector[i] = max(vector[i], search_space[i][0])
        vector[i] = min(vector[i], search_space[i][1])

    return {'vector': vector}


def mean_attr(samples, i):
    s = sum([sample['vector'][i] for sample in samples])
    return s / len(samples)


def stdev_attr(samples, mean, i):
    s = sum([(sample['vector'][i] - mean)**2.0 for sample in samples])
    return math.sqrt(s / len(samples))


def update_distribution(samples, alpha, means, stdevs):
    for i in range(len(means)):
        means[i] = alpha*means[i] + ((1.0-alpha)*mean_attr(samples, i))
        stdevs[i] = alpha*stdevs[i] + \
            ((1.0-alpha)*stdev_attr(samples, means[i], i))


def search(bounds, max_iter, num_samples, num_update, learning_rate):
    means = [random_variable(bounds[i]) for i in range(len(bounds))]
    stdevs = [bounds[i][1]-bounds[i][0] for i in range(len(bounds))]
    best = None
    for i in range(max_iter):
        samples = [generate_sample(bounds, means, stdevs)
                   for i in range(num_samples)]
        for samp in samples:
            samp['cost'] = objective_function(samp['vector'])
        samples = sorted(samples, key=lambda x: x['cost'])
        if best is None or samples[0]['cost'] < best['cost']:
            best = samples[0]
        selected = samples[:num_update]
        update_distribution(selected, learning_rate, means, stdevs)

    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_iter = 100
    num_samples = 50
    num_update = 5
    l_rate = 0.7

    best = search(search_space, max_iter, num_samples, num_update, l_rate)
    print(best['cost'])
