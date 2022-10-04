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


def contains(vector, space):
    for i, v in enumerate(vector):
        if v < space[i][0] or v > space[i][1]:
            return False
    return True


def matches(vector, dataset, min_dist):
    for pattern in dataset:
        dist = euclidean_distance(vector, pattern['vector'])
        if dist <= min_dist:
            return True
    return False


def generate_detectors(max_detectors, search_space, self_dataset, min_dist):
    detectors = []
    while True:
        detector = {'vector': random_vector(search_space)}
        if not matches(detector['vector'], self_dataset, min_dist):
            if not matches(detector['vector'], detectors, 0):
                detectors.append(detector)
        if len(detectors) >= max_detectors:
            break
    return detectors


def generate_self_dataset(num_records, self_space, search_space):
    self_dataset = []
    while True:
        pattern = {}
        pattern['vector'] = random_vector(search_space)
        if matches(pattern['vector'], self_dataset, 0.0):
            continue
        if contains(pattern['vector'], self_space):
            self_dataset.append(pattern)
        if len(self_dataset) >= num_records:
            break
    return self_dataset


def apply_detectors(detectors, bounds, self_dataset, min_dist, trials=50):
    correct = 0
    for i in range(trials):
        input = {'vector': random_vector(bounds)}
        actual = 'N' if matches(input['vector'], detectors, min_dist) else 'S'
        expected = 'S' if matches(
            input['vector'], self_dataset, min_dist) else 'N'
        if actual == expected:
            correct += 1
        print(f"{i+1}/{trials}: predicted={actual}, expected={expected}")
    print(f"Done. Result: {correct}/{trials}")
    return correct


def execute(bounds, self_space, max_detect, max_self, min_dist):
    self_dataset = generate_self_dataset(max_self, self_space, bounds)
    print(f"Done: prepared {len(self_dataset)} self patterns.")
    detectors = generate_detectors(max_detect, bounds, self_dataset, min_dist)
    print(f"Done: prepared {len(detectors)} detectors.")
    apply_detectors(detectors, bounds, self_dataset, min_dist)
    return detectors


if __name__ == '__main__':
    problem_size = 2
    search_space = [[0, 1] for _ in range(problem_size)]
    self_space = [[0.5, 1] for _ in range(problem_size)]
    max_self = 150
    max_detectors = 300
    min_dist = 0.05
    num_rand = 2
    execute(search_space, self_space, max_detectors, max_self, min_dist)
