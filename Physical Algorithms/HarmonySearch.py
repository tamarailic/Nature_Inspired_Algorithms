import random


def rand_in_bounds(lower_bound, upper_bound):
    return lower_bound + ((upper_bound-lower_bound) * random.random())


def random_vector(search_space):
    return [rand_in_bounds(search_space[i][0], search_space[i][1]) for i in range(len(search_space))]


def objective_function(vector):
    return sum([x**2 for x in vector])


def create_random_harmony(search_space):
    harmony = {}
    harmony['vector'] = random_vector(search_space)
    harmony['fitness'] = objective_function(harmony['vector'])
    return harmony


def initialize_harmony_memory(search_space, mem_size, factor=3):
    memory = [create_random_harmony(search_space)
              for _ in range(mem_size * factor)]
    memory = sorted(memory, key=lambda x: x['fitness'])
    return memory[:mem_size]


def create_harmony(search_space, memory, consid_rate, adjust_rate, r):
    vector = [0] * len(search_space)
    for i in range(len(search_space)):
        if random.random() < consid_rate:
            value = memory[random.randint(0, len(memory) - 1)]['vector'][i]
            if random.random() < adjust_rate:
                value = value + r * rand_in_bounds(-1, 1)
            value = min(search_space[i][1], value)
            value = max(search_space[i][0], value)
            vector[i] = value
        else:
            vector[i] = rand_in_bounds(search_space[i][0], search_space[i][1])
    return {'vector': vector}


def search(bounds, max_iter, mem_size, consid_rate, adjust_rate, r):
    memory = initialize_harmony_memory(bounds, mem_size)
    best = memory[0]
    for i in range(max_iter):
        harm = create_harmony(bounds, memory, consid_rate, adjust_rate, r)
        harm['fitness'] = objective_function(harm['vector'])
        if harm['fitness'] < best['fitness']:
            best = harm
        memory.append(harm)
        memory = sorted(memory, key=lambda x: x['fitness'])
        memory.pop(-1)
    return best


if __name__ == '__main__':

    problem_size = 3
    bounds = [[-5, 5] for _ in range(problem_size)]

    mem_size = 20
    consid_rate = 0.95
    adjust_rate = 0.7
    r = 0.05
    max_iter = 500
    best = search(bounds, max_iter, mem_size, consid_rate, adjust_rate, r)
    print(best['fitness'])
