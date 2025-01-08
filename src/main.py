from wgd_estimate import estimate_score_with_wgd, read_data_from_csv, read_data_from_yaml
from glicko_estimate import estimate_score_with_glicko

DATA_FILE = './data/questions_data.yaml'  # or './data/questions_data.csv'
# only for test
# DATA_FILE = './data/test_data.csv'
# DATA_FILE = './data/test_data.yaml'
USE_GLICKO = True  # Default to using Glicko method

# for glicko method
INITIAL_SCORE = 1580
INITIAL_RD = 350
INITIAL_VOL = 0.06

# for WGD method.
LEARNING_RATE = 0.1
MAX_ITER = 2000
DECAY_FACTOR = 0.99


def main():
    # Read data
    if DATA_FILE.endswith('.csv'):
        data = read_data_from_csv(DATA_FILE)
    else:
        data = read_data_from_yaml(DATA_FILE)

    if USE_GLICKO:
        # Estimate score using Glicko
        print("\nEstimating score using Glicko...")
        estimated_score, confidence_interval = estimate_score_with_glicko(
            data, initial_score=INITIAL_SCORE, initial_rd=INITIAL_RD, initial_volatility=INITIAL_VOL)

        # Output Glicko results
        print(f"\nGlicko Final Estimated Score: {estimated_score:.2f}")
        print(f"Glicko 95% Confidence Interval: ({confidence_interval[0]:.2f}, {
              confidence_interval[1]:.2f})")
    else:
        # Estimate score using WGD
        print("Estimating score using WGD...")
        estimated_score, confidence_interval = estimate_score_with_wgd(
            data, initial_score=INITIAL_SCORE, learning_rate=LEARNING_RATE,
            max_iter=MAX_ITER, decay_factor=DECAY_FACTOR
        )

        # Output WGD results
        print(f"\nWGD Final Estimated Score: {estimated_score:.2f}")
        print(f"WGD 95% Confidence Interval: ({confidence_interval[0]:.2f}, {
              confidence_interval[1]:.2f})")


if __name__ == "__main__":
    main()
