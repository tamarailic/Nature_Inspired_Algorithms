import random
import math


def rand_in_bounds(lower_bound, upper_bound):
    return lower_bound + ((upper_bound-lower_bound) * random.random())


def random_vector(search_space):
    return [rand_in_bounds(search_space[i][0], search_space[i][1]) for i in range(len(search_space))]


def distance(c1, c2):
    s = 0
    for i in range(len(c1)):
        s += (c1[i]-c2[i])**2.0
    return math.sqrt(s)


def create_cell(vector, class_label):
    return {'label': class_label, 'vector': vector}


def initialize_cells(domain):
    mem_cells = []
    for key in domain.keys():
        mem_cells.append(create_cell(random_vector([[0, 1], [0, 1]]), key))
    return mem_cells


def generate_random_pattern(domain):
    class_label = list(domain.keys())[
        random.randint(0, len(domain.keys()) - 1)]
    pattern = {'label': class_label}
    pattern['vector'] = random_vector(domain[class_label])
    return pattern


def stimulate(cells, pattern):
    max_dist = distance([0.0, 0.0], [1.0, 1.0])
    for cell in cells:
        cell['affinity'] = distance(
            cell['vector'], pattern['vector']) / max_dist
        cell['stimulation'] = 1.0 - cell['affinity']


def get_most_stimulated_cell(mem_cells, pattern):
    stimulate(mem_cells, pattern)
    return sorted(mem_cells, key=lambda x: x['stimulation'], reverse=True)[0]


def mutate_cell(cell, best_match):
    range = 1 - best_match['stimulation']
    for i, v in enumerate(cell['vector']):
        mini = max(v - range/2, 0)
        maxi = min(v + range/2, 1)
        cell['vector'][i] = mini + (random.random() * (maxi - mini))
    return cell


def create_arb_pool(pattern, best_match, clone_rate, mutate_rate):
    pool = []
    pool.append(create_cell(best_match['vector'], best_match['label']))
    num_clones = round(best_match['stimulation'] * clone_rate * mutate_rate)
    for _ in range(num_clones):
        cell = create_cell(best_match['vector'], best_match['label'])
        pool.append(mutate_cell(cell, best_match))
    return pool


def competition_for_resournces(pool, clone_rate, max_res):
    for cell in pool:
        cell['resources'] = cell['stimulation'] * clone_rate
    #pool = sorted(pool, key=lambda x: x['resources'])
    total_resources = sum([c['resources'] for c in pool])
    while total_resources > max_res:
        cell = pool.pop(len(pool) - 1)
        total_resources -= cell['resources']


def refine_arb_pool(pool, pattern, stim_thresh, clone_rate, max_res):
    mean_stim, candidate = 0, None
    while True:
        stimulate(pool, pattern)
        candidate = sorted(
            pool, key=lambda x: x['stimulation'], reverse=True)[0]
        mean_stim = sum([c['stimulation'] for c in pool])/len(pool)
        if mean_stim < stim_thresh:
            candidate = competition_for_resournces(pool, clone_rate, max_res)
            for i in range(len(pool)):
                cell = create_cell(pool[i]['vector'], pool[i]['label'])
                mutate_cell(cell, pool[i])
                pool.append(cell)
        if mean_stim >= stim_thresh:
            break
    return candidate


def add_candidate_to_memory_pool(candidate, best_match, mem_cells):
    if candidate['stimulation'] > best_match['stimulation']:
        mem_cells.append(candidate)


def train_system(mem_cells, domain, num_patterns, clone_rate, mutate_rate,
                 stim_thresh, max_res):
    for i in range(num_patterns):
        pattern = generate_random_pattern(domain)
        best_match = get_most_stimulated_cell(mem_cells, pattern)
        if best_match['label'] != pattern['label']:
            mem_cells.append(create_cell(pattern['vector'], pattern['label']))
        elif best_match['stimulation'] < 1:
            pool = create_arb_pool(pattern, best_match,
                                   clone_rate, mutate_rate)
            cand = refine_arb_pool(
                pool, pattern, stim_thresh, clone_rate, max_res)
            add_candidate_to_memory_pool(cand, best_match, mem_cells)
        print(
            f" > iter={i+1}, mem_cells={len(mem_cells)}, pool_size={len(pool)}")


def classify_pattern(mem_cells, pattern):
    stimulate(mem_cells, pattern)
    return sorted(mem_cells, key=lambda x: x['stimulation'], reverse=True)[0]


def test_system(mem_cells, domain, num_trials=50):
    correct = 0
    for _ in range(num_trials):
        pattern = generate_random_pattern(domain)
        best = classify_pattern(mem_cells, pattern)
        if pattern['label'] == best['label']:
            correct += 1
    print(f"Finished test with a score of {correct}/{num_trials}")
    return correct


def execute(domain, num_patterns, clone_rate, mutate_rate, stim_thresh,
            max_res):
    mem_cells = initialize_cells(domain)
    train_system(mem_cells, domain, num_patterns, clone_rate, mutate_rate,
                 stim_thresh, max_res)
    test_system(mem_cells, domain)
    return mem_cells


if __name__ == '__main__':
    domain = {"A": [[0, 0.4999999], [0, 0.4999999]], "B": [[0.5, 1], [0.5, 1]]}
    num_patterns = 50
    clone_rate = 10
    mutate_rate = 2.0
    stim_thresh = 0.9
    max_res = 150
    execute(domain, num_patterns, clone_rate, mutate_rate, stim_thresh,
            max_res)
