import random


def rand_in_bounds(lower_bound, upper_bound):
    return lower_bound + ((upper_bound-lower_bound) * random.random())


def random_vector(search_space):
    return [rand_in_bounds(search_space[i][0], search_space[i][1]) for i in range(len(search_space))]


def initialize_cell(thresh, cell=None):
    if cell is None:
        cell = {}
    cell['lifespan'] = 1000.0
    cell['k'] = 0.0
    cell['cms'] = 0.0
    cell['migration_threshold'] = rand_in_bounds(thresh[0], thresh[1])
    cell['antigen'] = {}
    return cell


def construct_pattern(class_label, domain, p_safe, p_danger):
    set = domain[class_label]
    selection = random.randint(0, len(set) - 1)
    pattern = {}
    pattern['class_label'] = class_label
    pattern['input'] = set[selection]
    pattern['safe'] = (random.random() * p_safe * 100)
    pattern['danger'] = (random.random() * p_danger * 100)
    return pattern


def generate_pattern(domain, p_anomaly, p_normal, prob_create_anom=0.5):
    pattern = None
    if random.random() < prob_create_anom:
        pattern = construct_pattern("Anomaly", domain, 1.0-p_normal, p_anomaly)
    else:
        pattern = construct_pattern("Normal", domain, p_normal, 1.0-p_anomaly)
    return pattern


def store_antigen(cell, input):
    if cell['antigen'].get(input) == None:
        cell['antigen'][input] = 1
    else:
        cell['antigen'][input] += 1


def expose_cell(cell, cms, k, pattern, immature_cells):
    cell['cms'] += cms
    cell['k'] += k
    cell['lifespan'] -= cms
    store_antigen(cell, pattern['input'])
    if cell['lifespan'] <= 0:
        immature_cells.remove(cell)


def can_cell_migrate(cell):
    if (cell['cms'] >= cell['migration_threshold']):
        if bool(cell['antigen']):
            return True
    return False


def expose_all_cells(immature_cells, domain, p_anomaly, p_normal):
    migrate = []
    for cell in immature_cells:
        pattern = generate_pattern(domain, p_anomaly, p_normal)
        cms = (pattern['safe'] + pattern['danger'])
        k = pattern['danger'] - (pattern['safe'] * 2)
        expose_cell(cell, cms, k, pattern, immature_cells)
        if can_cell_migrate(cell):
            cell['class_label'] = "Anomaly" if cell['k'] > 0 else "Normal"
            migrate.append(cell)
    return migrate


def train_system(domain, max_iter, num_cells, p_anomaly, p_normal, thresh):
    immature_cells = [initialize_cell(thresh) for _ in range(num_cells)]
    migrated = []
    for _ in range(max_iter):
        migrants = expose_all_cells(
            immature_cells, domain, p_anomaly, p_normal)
        migrated = [c for c in migrants]
        for cell in migrants:
            immature_cells.remove(cell)
            immature_cells.append(initialize_cell(thresh))

    return migrated


def classify_pattern(migrated, pattern):
    input = pattern['input']
    num_cells, num_antigen = 0, 0
    for cell in migrated:
        if cell['class_label'] == "Anomaly" and not cell['antigen'].get(input) == None:
            num_cells += 1
            num_antigen += cell['antigen'][input]
    try:
        mcav = num_cells / num_antigen
    except:
        mcav = 0
    if mcav > 0.5:
        return "Anomaly"
    return "Normal"


def test_system(migrated, domain, p_anomaly, p_normal, num_trial=100):
    correct_norm = 0
    for _ in range(num_trial):
        pattern = construct_pattern("Normal", domain, p_normal, 1.0-p_anomaly)
        class_label = classify_pattern(migrated, pattern)
        if class_label == "Normal":
            correct_norm += 1
    print(f"Finished testing Normal inputs {correct_norm}/{num_trial}")
    correct_anom = 0
    for _ in range(num_trial):
        pattern = construct_pattern("Anomaly", domain, 1.0-p_normal, p_anomaly)
        class_label = classify_pattern(migrated, pattern)
        if class_label == "Anomaly":
            correct_anom += 1
    print(f"Finished testing Anomaly inputs {correct_anom}/{num_trial}")


def execute(domain, max_iter, num_cells, p_anom, p_norm, thresh):
    migrated = train_system(domain, max_iter, num_cells,
                            p_anom, p_norm, thresh)
    test_system(migrated, domain, p_anom, p_norm)
    return migrated


if __name__ == '__main__':
    domain = {}
    domain["Normal"] = [i for i in range(50) if i % 10 != 0]
    domain["Anomaly"] = [(i+1)*10 for i in range(5)]
    p_anomaly = 0.70
    p_normal = 0.95
    iterations = 1000
    num_cells = 10
    thresh = [5, 15]
    execute(domain, iterations, num_cells, p_anomaly, p_normal, thresh)
