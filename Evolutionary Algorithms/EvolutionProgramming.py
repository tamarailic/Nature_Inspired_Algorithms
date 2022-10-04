import random
import math


def generate_space(lower_bound, upper_bound):
    space = []
    for _ in range(problem_size):
        space.append([lower_bound, upper_bound])

    return space


def init_population():
    strategy = []
    population = []
    for i in range(problem_size):
        strategy.append([0, (search_space[i][1] - search_space[i][0]) * 0.05])

    for _ in range(pop_size):
        member = {}
        member['vector'] = random_vector(search_space)
        member['strategy'] = random_vector(strategy)
        population.append(member)

    for member in population:
        member['fitness'] = objective_function(member['vector'])

    return population


def random_vector(space):
    vector = []

    for i in range(len(search_space)):
        vector.append(space[i][0] + (space[i][1] -
                      space[i][0]) * random.random())

    return vector


def objective_function(vector):
    sum = 0
    for v in vector:
        sum += v ** 2

    return sum


def random_gaussian(mean=0, stdev=1):
    u1, u2, w = 0, 0, 0
    while True:
        u1 = 2 * random.random() - 1
        u2 = 2 * random.random() - 1
        w = u1 * u1 + u2 * u2
        if w < 1:
            break
    w = math.sqrt((-2 * math.log(w)) / w)
    return mean + (u2 * w) * stdev


def mutate(member):
    child = {'vector': [0] * problem_size, 'strategy': [0] * problem_size}
    for i in range(problem_size):
        s_old = member['strategy'][i]
        v_old = member['vector'][i]
        v = v_old + s_old * random_gaussian()
        v = min(search_space[i][1], v)
        v = max(search_space[i][0], v)
        child['vector'][i] = v
        child['strategy'][i] = s_old + random_gaussian() * abs(s_old) ** 0.5
    return child


def tournament(member, population):
    wins = 0
    for _ in range(bout_size):
        other = population[random.randint(0, pop_size - 1)]
        if member['fitness'] < other['fitness']:
            wins += 1
    return wins


def search():
    population = init_population()
    best = sorted(population, key=lambda x: x['fitness'])[0]
    for _ in range(max_gens):
        children = []
        for i in range(pop_size):
            children.append(mutate(population[i]))

        for child in children:
            child['fitness'] = objective_function(child['vector'])
        children = sorted(children, key=lambda x: x['fitness'])
        if children[0]['fitness'] < best['fitness']:
            best = children[0]
        union = [] + children + population
        # for member in union:
        #     member['wins'] = tournament(member, union)
        # union = sorted(union, key=lambda x: x['wins'])
        union = sorted(union, key=lambda x: x['fitness'])
        union_best = union[0]
        if union_best['fitness'] < best['fitness']:
            best = union[0]
        population = union[:pop_size]
    return best


if __name__ == '__main__':
    problem_size = 2
    pop_size = 100
    search_space = generate_space(-5, 5)
    max_gens = 200
    bout_size = 5
    best = search()
    print(best['fitness'])
