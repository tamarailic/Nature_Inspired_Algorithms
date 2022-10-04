import random


def calculate_error(pref):
    s = 0
    for p in pref:
        s += p['error']/len(pref)

    return round(s)


def calculate_acc(pref):
    s = 0
    for p in pref:
        s += p['correct']/len(pref)

    return s


def random_bitstring(num_bits=6):
    bitstring = ''
    for _ in range(num_bits):
        random_chance = random.random()
        if random_chance >= 0.5:
            bitstring += '1'
        else:
            bitstring += '0'

    return bitstring


def does_match(input, condition):
    for i in range(len(input)):
        if condition[i] == '#' and input[i] == condition[i]:
            return False
    return True


def get_actions(pop):
    actions = []
    for i in range(len(pop)):
        if not (pop[i]['action'] in actions):
            actions.append(pop[i]['action'])
    return actions


def new_classifier(condition, action, gen, p1=10, e1=0, f1=10):
    other = {}
    other['condition'], other['action'], other['last_time'] = condition, action, gen
    other['pred'], other['error'], other['fitness'] = p1, e1, f1
    other['exp'], other['setsize'], other['num'] = 0, 1, 1
    return other


def generate_random_classifier(input, actions, gen, rate=1/3):
    condition = ''
    for i in range(len(input)):
        if random.random() < rate:
            condition += '#'
        else:
            condition += input[i]
    action = actions[random.randint(0, len(actions) - 1)]
    return new_classifier(condition, action, gen)


def calculate_deletion_vote(classifier, pop, del_tresh, f_tresh=1):
    vote = classifier['setsize'] * classifier['num']
    total = sum([member['num'] for member in pop])
    avg_fitness = sum([member['fitness'] for member in pop])
    avg_fitness = avg_fitness / total
    derated = classifier['fitness'] / classifier['num']
    if classifier['exp'] > del_tresh and derated < (f_tresh * avg_fitness):
        return vote * (avg_fitness / derated)
    return vote


def delete_from_pop(pop, pop_size, del_tresh=20):
    total = sum([member['num'] for member in pop])
    if total <= pop_size:
        return pop
    for member in pop:
        member['dvote'] = calculate_deletion_vote(member, pop, del_tresh)
    vote_sum = sum([member['dvote'] for member in pop])
    point = random.random() * vote_sum
    vote_sum, index = 0, 0
    for i in range(len(pop)):
        vote_sum += pop[i]['dvote']
        if vote_sum >= point:
            index = i
            break
    if pop[index]['num'] > 1:
        pop[index]['num'] -= 1
    else:
        del pop[index]
    return pop


def generate_match_set(input, pop, all_actions, gen, pop_size):
    match_set = [member for member in pop if does_match(
        input, member['condition'])]
    actions = get_actions(match_set)
    while len(actions) < len(all_actions):
        remaining = [action for action in all_actions if action not in actions]
        classifier = generate_random_classifier(input, remaining, gen)
        pop.append(classifier)
        match_set.append(classifier)
        pop = delete_from_pop(pop, pop_size)
        actions.append(classifier['action'])
    return match_set


def generate_predictions(match_size):
    pred = {}
    for i in range(len(match_size)):
        key = match_size[i]['action']
        if key not in pred.keys():
            pred[key] = {'sum': 0, 'count': 0, 'weight': 0}
        pred[key]['sum'] += match_size[i]['pred'] * match_size[i]['fitness']
        pred[key]['count'] += match_size[i]['fitness']

    for key in pred.keys():
        pred[key]['weight'] = 0
        if pred[key]['count'] > 0:
            pred[key]['weight'] = pred[key]['sum'] / pred[key]['count']
    return pred


def select_action(predicitons, p_explore=False):
    keys = list(predicitons.keys())
    if p_explore:
        return keys[random.randint(0, len(keys) - 1)]
    keys = sorted(keys, key=lambda x: predicitons[x]['weight'], reverse=True)
    return keys[0]


def neg(bit):
    return 0 if (bit == 1) else 1


def target_function(s):
    ints = [int(s[i]) for i in range(6)]
    x0, x1, x2, x3, x4, x5 = ints
    return neg(x0) * neg(x1) * x2 + neg(x0) * x1 * x3 + x0 * neg(x1) * x4 + x0 * x1 * x5


def update_set(action_set, reward, beta=0.2):
    s = sum([other['num'] for other in action_set])
    for action in action_set:
        action['exp'] += 1
        if action['exp'] < 1/beta:
            action['error'] = abs(
                action['error'] * (action['exp'] - 1) + (reward - action['pred'])) / action['exp']
            action['pred'] = (
                action['pred'] * (action['exp'] - 1) + reward) / action['exp']
            action['setsize'] = (action['setsize'] *
                                 (action['exp'] - 1) + s) / action['exp']
        else:
            action['error'] += beta * \
                abs(reward - action['pred']) - action['error']
            action['pred'] += beta * (reward - action['pred'])
            action['setsize'] += beta * (s - action['setsize'])
    return action_set


def update_fitness(action_set, min_error=10, l_rate=0.2, alpha=0.1, v=-5):
    sum = 0
    acc = [0] * len(action_set)
    for i in range(len(action_set)):
        if action_set[i]['error'] < min_error:
            acc[i] = 1
        else:
            acc[i] = alpha*(action_set[i]['error'] / min_error) ** v
        sum += acc[i] * action_set[i]['num']

    for i in range(len(action_set)):
        action_set[i]['fitness'] = l_rate * \
            ((acc[i] * action_set[i]['num']) / sum - action_set[i]['fitness'])
    return action_set


def can_run_genetic_algorithm(action_set, gen, ga_freq):
    if len(action_set) <= 2:
        return False
    total = sum([member['last_time'] + member['num'] for member in action_set])
    s = sum([member['num'] for member in action_set])
    if gen - (total/sum) > ga_freq:
        return True
    return False


def binary_tournament(pop):
    i, j = random.randint(0, pop.size), random.randint(0, pop.size)
    while j == i:
        j = random.randint(0, pop.size)
    return pop[i] if (pop[i]['fitness'] > pop[j]['fitness']) else pop[j]


def copy_classifier(parent):
    copy = {}
    for key in parent.keys():
        copy[key] = parent[key] if type(parent[key]) == str else parent[key]
    copy['num'], copy['exp'] = 1, 0
    return copy


def uniform_crossover(parent1, parent2):
    child = ""
    for i in range(len(parent1)):
        child.append(parent1[i] if random.random() < 0.5 else parent2[i])

    return child


def crossover(c1, c2, p1, p2):
    c1['condition'] = uniform_crossover(p1['condition'], p2['condition'])
    c2['condition'] = uniform_crossover(p1['condition'], p2['condition'])
    c1['pred'] = (p1['pred'] + p2['pred']) / 2
    c1['error'] = 0.25 * (p1['error'] + p2['error']) / 2
    c1['fitness'] = 0.1 * (p1['fitness'] + p2['fitness']) / 2


def mutation(cl, action_set, input, rate=0.04):
    for i in range(len(cl['condition'])):
        if random.random() < rate:
            cl['condition'][i] = input[i] if (
                cl['condition'][i] == ' #') else '#'

        if random.random() < rate:
            subset = action_set - [cl['action']]
            cl['action'] = subset[random.randint(0, len(subset) - 1)]


def insert_in_pop(cla, pop):
    for member in pop:
        if cla['condition'] == member['condition'] and cla['action'] == member['action']:
            member['num'] += 1
            return
    pop.append(cla)
    return pop


def run_ga(actions, pop, action_set, input, gen, pop_size, crate=0.8):
    p1, p2 = binary_tournament(action_set), binary_tournament(action_set)
    c1, c2 = copy_classifier(p1), copy_classifier(p2)
    if random.random() < crate:
        crossover(c1, c2, p1, p2)
    for c in [c1, c2]:
        mutation(c, actions, input)
        pop = insert_in_pop(c, pop)
    while sum([member['num'] for member in pop]) > pop_size:
        pop = delete_from_pop(pop, pop_size)


def train_model(pop_size, max_gens, actions, ga_freq):
    pop, pref = [], []
    for gen in range(max_gens):
        explore = gen % 2 == 0
        input = random_bitstring()
        match_set = generate_match_set(input, pop, actions, gen, pop_size)
        pred_array = generate_predictions(match_set)
        action = select_action(pred_array, explore)
        reward = 1000 if target_function(input) == int(action) else 0
        if explore:
            action_set = [
                candidate for candidate in match_set if candidate['action'] == action]
            action_set = update_set(action_set, reward)
            action_set = update_fitness(action_set)
            if can_run_genetic_algorithm(action_set, gen, ga_freq):
                for action in action_set:
                    action['last_time'] = gen
                run_ga(actions, pop, action_set, input, gen, pop_size)
        else:
            e, a = abs(pred_array[action]['weight'] -
                       reward), (1 if reward == 1000 else 0)
            pref.append({'error': e, 'correct': a})
            if len(pref) >= 50:
                err = calculate_error(pref)
                acc = calculate_acc(pref)
                pref = []
    return pop


def test_model(system, num_trails=50):
    correct = 0
    for _ in range(num_trails):
        input = random_bitstring()
        match_set = [member for member in system if does_match(
            input, member['condition'])]
        pred_array = generate_predictions(match_set)
        action = select_action(pred_array, False)
        print(target_function(input), action)
        if int(target_function(input)) == int(action):
            correct += 1

    return correct


def execute(pop_size, max_gens, actions, ga_freq):
    system = train_model(pop_size, max_gens, actions, ga_freq)
    print(test_model(system))
    return system


if __name__ == '__main__':
    all_actions = ['0', '1']
    max_gens = 5000
    pop_size = 200
    ga_freq = 25
    print(execute(pop_size, max_gens, all_actions, ga_freq))
