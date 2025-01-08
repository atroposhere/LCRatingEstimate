import csv
import math
import yaml
import numpy as np


def get_expected_score(score, actual_score):
    return 1 / (1 + 10 ** ((score - actual_score) / 400))


def estimate_score_with_iteration(data, initial_score=1580, learning_rate=0.1, max_iter=10000, decay_factor=0.9):
    score = initial_score

    # Perform first max_iter - 1 iterations
    for iteration in range(max_iter - 1):
        total_diff = 0
        for i, (topic_score, passed_flag) in enumerate(data):
            # Calculate weight based on sample order, giving more weight to newer samples
            # Decaying weight (e.g., recent samples have higher weight, older samples have lower weight)
            weight = decay_factor ** (len(data) - i)

            actual_rate = 1 if passed_flag else 0
            expected_rate = get_expected_score(topic_score, score)

            # Calculate and weight the error
            diff = (actual_rate - expected_rate) * \
                400  # ELO rating update error
            total_diff += weight * diff

        # Update score using weighted gradient descent
        score += learning_rate * total_diff / len(data)
        print(f"Iteration {iteration+1}: Estimated Score = {score:.2f}")

    # Perform final iteration to calculate errors and weights
    weighted_squared_errors = []  # Store weighted squared errors
    weights = []  # Store sample weights
    total_diff = 0

    for i, (topic_score, passed_flag) in enumerate(data):
        # Calculate weight based on sample order, giving more weight to newer samples
        weight = decay_factor ** (len(data) - i)  # Decaying weight

        actual_rate = 1 if passed_flag else 0
        expected_rate = get_expected_score(topic_score, score)

        # Calculate and weight the error
        diff = (actual_rate - expected_rate) * 400  # ELO rating update error
        total_diff += weight * diff

        # Calculate and store weighted squared error
        weighted_squared_errors.append(diff ** 2)
        weights.append(weight)

    # Update score using weighted gradient descent
    score += learning_rate * total_diff / len(data)
    print(f"Iteration {max_iter}: Estimated Score = {score:.2f}")

    # Calculate weighted standard error
    weighted_squared_errors = np.array(weighted_squared_errors)
    weights = np.array(weights)

    # Calculate weighted variance
    weighted_squared_errors = weighted_squared_errors * weights
    weighted_variance = weighted_squared_errors.sum() / weights.sum()  # Weighted variance
    standard_error = math.sqrt(weighted_variance) / \
        math.sqrt(len(data))  # Weighted standard error
    confidence_interval = (score - 1.96 * standard_error,
                           score + 1.96 * standard_error)

    return score, confidence_interval


def read_data_from_csv(filename='./data/questions_data.csv'):
    data = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip CSV header
        for row in reader:
            score = int(row[0])
            passed_flag = row[1] == 'True'
            data.append((score, passed_flag))
    return data


def read_data_from_yaml(filename='./data/questions_data.yaml'):
    """
    Read and parse YAML data file containing question scores and results.
    """
    # Read YAML file
    with open(filename, 'r') as f:
        raw_data = yaml.safe_load(f)

    # Extract data and convert to numpy array
    data = [[item["topic_score"], item["passed"]] for item in raw_data["data"]]

    return data


if __name__ == "__main__":
    # data = read_data_from_csv()
    data = read_data_from_yaml()
    cur_ratings = 1574.2
    estimated_score, confidence_interval = estimate_score_with_iteration(
        data, cur_ratings, learning_rate=0.1, max_iter=1000, decay_factor=0.99)
    print(f"\nFinal Estimated Score: {estimated_score:.2f}")
    print(
        f"95% Confidence Interval: ({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})")
