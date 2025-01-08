from estimate import estimate_score_with_iteration, read_data_from_csv, read_data_from_yaml

# Constants
INITIAL_SCORE = 1580
LEARNING_RATE = 0.1
MAX_ITER = 5000
DECAY_FACTOR = 0.9
DATA_FILE = './data/questions_data.yaml'  # or './data/questions_data.csv'


def main():
    # Read data
    if DATA_FILE.endswith('.csv'):
        data = read_data_from_csv(DATA_FILE)
    else:
        data = read_data_from_yaml(DATA_FILE)

    # Estimate score
    estimated_score, confidence_interval = estimate_score_with_iteration(
        data, initial_score=INITIAL_SCORE, learning_rate=LEARNING_RATE,
        max_iter=MAX_ITER, decay_factor=DECAY_FACTOR
    )

    # Output results
    print(f"\nFinal Estimated Score: {estimated_score:.2f}")
    print(f"95% Confidence Interval: ({confidence_interval[0]:.2f}, {
          confidence_interval[1]:.2f})")


if __name__ == "__main__":
    main()
