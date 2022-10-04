
import math
import random


def random_permutation(cities):
    perm = [i for i in range(len(cities))]
    for i in range(len(cities)):
        r = random.randint(0, len(perm) - 1 - i) + i
        perm[r], perm[i] = perm[i], perm[r]
    return perm


def euc_2d(city1, city2):
    return round(math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2))


def cost(permutation, cities):
    distance = 0
    for i, city in enumerate(permutation):
        city2 = permutation[0] if i == len(
            permutation) - 1 else permutation[i + 1]
        distance += euc_2d(cities[city], cities[city2])
    return distance


def get_edges_for_city(city_number, perm):
    c1, c2 = None, None
    for i, city in enumerate(perm):
        if city == city_number:
            c1 = perm[-1] if i == 0 else perm[i - 1]
            c2 = perm[0] if i == len(perm) - 1 else perm[i + 1]
            break
    return c1, c2


def calculate_neighbor_rank(city_number, cities, ignore=[]):
    neighbors = []
    for i, city in enumerate(cities):
        if i == city_number or i in ignore:
            continue
        neighbor = {'number': i}
        neighbor['distance'] = euc_2d(cities[city_number], city)
        neighbors.append(neighbor)
    return sorted(neighbors, key=lambda x: x['distance'])


def calculate_city_fitness(perm, city_number, cities):
    c1, c2 = get_edges_for_city(city_number, perm)
    neighbors = calculate_neighbor_rank(city_number, cities)
    n1, n2 = -1, 1
    for i, n in enumerate(neighbors):
        if n['number'] == c1:
            n1 = i + 1
        if n['number'] == c2:
            n2 = i + 1
        if n1 != -1 and n2 != -1:
            break
    return 3.0 / (n1 + n2)


def calculate_city_fitnesses(cities, perm):
    city_fitnesses = []
    for i, city in enumerate(cities):
        city_fitness = {'number': i}
        city_fitness['fitness'] = calculate_city_fitness(perm, i, cities)
        city_fitnesses.append(city_fitness)
    return sorted(city_fitnesses, key=lambda x: x['fitness'])


def calculate_component_probabilities(ordered_components, tau):
    s = 0
    for i, component in enumerate(ordered_components):
        component['prob'] = (i + 1)**(-tau)
        s += component['prob']
    return s


def make_selection(components, sum_probability):
    selection = random.random()
    for i, component in enumerate(components):
        selection -= (component['prob'] / sum_probability)
        if selection <= 0:
            return component['number']
    return components[-1]['number']


def probabilistic_selection(ordered_components, tau, exclude=[]):
    s = calculate_component_probabilities(ordered_components, tau)
    selected_city = None
    while True:

        selected_city = make_selection(ordered_components, s)
        if selected_city not in exclude:
            break
    return selected_city


def get_long_edge(edges, neighbor_distances):
    n1 = [d for d in neighbor_distances if d['number'] == edges[0]][0]
    n2 = [d for d in neighbor_distances if d['number'] == edges[1]][0]
    if n1['distance'] > n2['distance']:
        return n1['number']
    else:
        return n2['number']


def very_permutation(permutation, selected, new, long_edge):
    perm = [p for p in permutation]
    c1, c2 = perm[::-1].index(selected), perm[::-1].index(new)
    if c1 < c2:
        p1, p2 = c1, c2
    else:
        p1, p2 = c2, c1
    right = 0 if c1 == len(perm) - 1 else c1 + 1
    if perm[right] == long_edge:
        perm[p1 + 1:p2 + 1] = reversed(perm[p1 + 1:p2 + 1])
    else:
        perm[p1:p2] = reversed(perm[p1:p2])
    return perm


def create_new_perm(cities, tau, perm):
    city_fitness = calculate_city_fitnesses(cities, perm)
    selected_city = probabilistic_selection(city_fitness[::-1], tau)
    edges = get_edges_for_city(selected_city, perm)
    neighbors = calculate_neighbor_rank(selected_city, cities)
    new_neighbour = probabilistic_selection(neighbors, tau, edges)
    long_edge = get_long_edge(edges, neighbors)
    return very_permutation(perm, selected_city, new_neighbour, long_edge)


def search(cities, max_iterations, tau):
    current = {'vector': random_permutation(cities)}
    current['cost'] = cost(current['vector'], cities)
    best = current
    for _ in range(max_iterations):
        candidat = {}
        candidat['vector'] = create_new_perm(cities, tau, current['vector'])
        candidat['cost'] = cost(candidat['vector'], cities)
        current = candidat
        if current['cost'] < best['cost']:
            best = current
    return best


if __name__ == '__main__':
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655],
                [880, 660], [25, 230], [525, 1000], [
        580, 1175], [650, 1130], [1605, 620],
        [1220, 580], [1465, 200], [1530, 5], [
        845, 680], [725, 370], [145, 665],
        [415, 635], [510, 875], [560, 365], [
        300, 465], [520, 585], [480, 415],
        [835, 625], [975, 580], [1215, 245], [
        1320, 315], [1250, 400], [660, 180],
        [410, 250], [420, 555], [575, 665], [
            1150, 1160], [700, 580], [685, 595],
        [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960],
        [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65],
        [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]

    max_iterations = 250
    tau = 1.8
    best = search(berlin52, max_iterations, tau)
    print(best['cost'])
