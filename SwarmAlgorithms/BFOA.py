import random
import math


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def objective_function(vector):
    return sum([v**2 for v in vector])


def generate_random_direction(problem_size):
    bounds = [[-1, 1] for _ in range(problem_size)]
    return random_vector(bounds)


def compute_cell_interaction(cell, cells, d, w):
    s = 0
    for other in cells:
        diff = 0
        for i in range(len(cell['vector'])):
            diff += (cell['vector'][i] - other['vector'][i]) ** 2
        s += d * math.exp(w*diff)
    return s


def attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep):
    attract = compute_cell_interaction(cell, cells, -d_attr, -w_attr)
    repel = compute_cell_interaction(cell, cells, h_rep, -w_rep)
    return attract + repel


def evaluate(cell, cells, d_attr, w_attr, h_rep, w_rep):
    cell['cost'] = objective_function(cell['vector'])
    cell['inter'] = attract_repel(cell, cells, d_attr, w_attr, h_rep, w_rep)
    cell['fitness'] = cell['cost'] + cell['inter']


def tumble_cell(search_space, cell, step_size):
    step = generate_random_direction(len(search_space))
    vector = [0] * len(search_space)
    for i in range(len(search_space)):
        vector[i] = cell['vector'][i] + step_size * step[i]
        vector[i] = min(search_space[i][1], vector[i])
        vector[i] = max(search_space[i][0], vector[i])
    return {'vector': vector}


def chemotaxis(cells, search_space, chem_steps, swim_length, step_size,
               d_attr, w_attr, h_rep, w_rep):
    best = None
    for _ in range(chem_steps):
        moved_cells = []
        for _, cell in enumerate(cells):
            sum_nutrients = 0
            evaluate(cell, cells, d_attr, w_attr, h_rep, w_rep)
            if best is None or cell['cost'] < best['cost']:
                best = cell
            sum_nutrients += cell['fitness']
            for _ in range(swim_length):
                new_cell = tumble_cell(search_space, cell, step_size)
                evaluate(new_cell, cells, d_attr, w_attr, h_rep, w_rep)
                if new_cell['cost'] < best['cost']:
                    best = new_cell
                if new_cell['fitness'] > cell['fitness']:
                    break
                cell = new_cell
                sum_nutrients += cell['fitness']
            cell['sum_nutrients'] = sum_nutrients
            moved_cells.append(cell)
        cells = moved_cells
    return best, cells


def search(search_space, pop_size, elim_disp_steps, repro_steps,
           chem_steps, swim_length, step_size, d_attr, w_attr, h_rep, w_rep,
           p_eliminate):
    best = None
    cells = [{'vector': random_vector(search_space)} for _ in range(pop_size)]
    for _ in range(elim_disp_steps):
        for _ in range(repro_steps):
            c_best, cells = chemotaxis(cells, search_space, chem_steps,
                                       swim_length, step_size, d_attr, w_attr, h_rep, w_rep)
            if best is None or c_best['cost'] < best['cost']:
                best = c_best
            cells = sorted(
                cells, key=lambda x: x['sum_nutrients'])
            cells = cells[:pop_size//2] + cells[:pop_size//2]
        for cell in cells:
            if random.random() <= p_eliminate:
                cell['vector'] = random_vector(search_space)
    return best


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    pop_size = 50
    step_size = 0.1  # Ci
    elim_disp_steps = 1  # Ned
    repro_steps = 4  # Nre
    chem_steps = 70  # Nc
    swim_length = 4  # Ns
    p_eliminate = 0.25  # Ped
    d_attr = 0.1
    w_attr = 0.2
    h_rep = d_attr
    w_rep = 10
    best = search(search_space, pop_size, elim_disp_steps, repro_steps,
                  chem_steps, swim_length, step_size, d_attr, w_attr, h_rep, w_rep,
                  p_eliminate)
    print(best['cost'])
