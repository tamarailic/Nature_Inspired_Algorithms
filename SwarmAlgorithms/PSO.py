

import random


def copy_vector(vector):
    new = []
    for v in vector:
        temp = v
        new.append(temp)
    return new


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def objective_function(vector):
    return sum([v**2 for v in vector])


def create_particle(search_space, vel_space):
    particle = {}
    particle['position'] = random_vector(search_space)
    particle['cost'] = objective_function(particle['position'])
    particle['b_position'] = copy_vector(particle['position'])
    particle['b_cost'] = particle['cost']
    particle['velocity'] = random_vector(vel_space)
    return particle


def get_global_best(population, current_best=None):
    population = sorted(population, key=lambda x: x['cost'])
    best = population[0]
    if current_best is None or best['cost'] <= current_best['cost']:
        current_best = {}
        current_best['position'] = copy_vector(best['position'])
        current_best['cost'] = objective_function(current_best['position'])
    return current_best


def update_velocity(particle, gbest, max_v, c1, c2):
    for i, v in enumerate(particle['velocity']):
        v1 = c1 * random.random() * \
            (particle['b_position'][i] - particle['position'][i])
        v2 = c2 * random.random() * \
            (gbest['position'][i] - particle['position'][i])
        particle['velocity'][i] = v + v1 + v2
        particle['velocity'][i] = min(max_v, particle['velocity'][i])
        particle['velocity'][i] = max(-max_v, particle['velocity'][i])


def update_position(part, bounds):
    for i, v in enumerate(part['position']):
        part['position'][i] = v + part['velocity'][i]
        if part['position'][i] > bounds[i][1]:
            part['position'][i] = bounds[i][1] - \
                abs(part['position'][i] - bounds[i][1])
            part['velocity'][i] *= -1


def update_best_position(particle):
    if particle['cost'] > particle['b_cost']:
        return
    particle['b_cost'] = particle['cost']
    particle['b_position'] = copy_vector(particle['position'])


def search(max_gens, search_space, vel_space, pop_size, max_vel, c1, c2):
    pop = [create_particle(search_space, vel_space) for _ in range(pop_size)]
    gbest = get_global_best(pop)
    for _ in range(max_gens):
        for particle in pop:
            update_velocity(particle, gbest, max_vel, c1, c2)
            update_position(particle, search_space)
            particle['cost'] = objective_function(particle['position'])
            update_best_position(particle)
        gbest = get_global_best(pop, gbest)

    return gbest


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    vel_space = [[-1, 1] for _ in range(problem_size)]
    max_gens = 100
    pop_size = 50
    max_vel = 100
    c1, c2 = 2, 2
    best = search(max_gens, search_space, vel_space, pop_size, max_vel, c1, c2)
    print(best['cost'])
