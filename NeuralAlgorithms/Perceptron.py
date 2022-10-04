import random


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def initialize_weights(problem_size):
    minmax = [[-1, 1] for _ in range(problem_size + 1)]
    return random_vector(minmax)


def activate(weights, vector):
    s = weights[len(weights) - 1] * 1
    for i, input in enumerate(vector):
        s += weights[i] * input
    return s


def transfer(activation):
    if activation >= 0:
        return 1
    return 0


def get_output(weights, vector):
    activation = activate(weights, vector)
    return transfer(activation)


def update_weights(num_inputs, weights, input, out_exp, out_act, l_rate):
    for i in range(num_inputs):
        weights[i] += l_rate * (out_exp - out_act) * input[i]
    weights[num_inputs] += l_rate * (out_exp - out_act) * 1.0


def train_weights(weights, domain, num_inputs, iterations, lrate):
    for epoch in range(iterations):
        error = 0
        for pattern in domain:
            input = [pattern[k] for k in range(num_inputs)]
            output = get_output(weights, input)
            expected = pattern[-1]
            error += abs(output - expected)
            update_weights(num_inputs, weights, input, expected, output, lrate)
        print(f"> epoch={epoch}, error={error}")


def test_weights(weights, domain, num_inputs):
    correct = 0
    random.shuffle(domain)
    for pattern in domain:
        input_vector = [pattern[k] for k in range(num_inputs)]
        output = get_output(weights, input_vector)
        if round(output) == pattern[-1]:
            correct += 1
    print(f"Finished test with a score of {correct}/{len(domain)}")
    return correct


def execute(domain, num_inputs, iterations, learning_rate):
    weights = initialize_weights(num_inputs)
    train_weights(weights, domain, num_inputs, iterations, learning_rate)
    test_weights(weights, domain, num_inputs)


if __name__ == '__main__':
    or_problem = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    inputs = 2
    iterations = 20
    learning_rate = 0.1
    execute(or_problem, inputs, iterations, learning_rate)
