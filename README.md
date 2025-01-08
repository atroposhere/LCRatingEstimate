# LeetCode Rating Estimate tools

This project is designed to help LeetCode users estimate their rating based on their recent problem-solving performance. The program uses a weighted ELO rating system to calculate an estimated rating and provides a 95% confidence interval for the estimate.

## Usage

### Prerequisites
- Python 3.x
- Required Python packages: `numpy`, `pyyaml`

You can install the required packages using pip:
```bash
pip install numpy pyyaml
```

### Generating Test Data
To generate random test data, you can use the `data_generator.py` script. This script generates both CSV and YAML files containing random problem scores and pass/fail flags.

```bash
python src/data_generator.py
```

By default, the script generates 100 samples and saves them to `./data/test_data.csv` and `./data/test_data.yaml`.

### Estimating LeetCode Rating
To estimate your LeetCode rating based on the generated data, use the `estimate.py` script:

```bash
python src/estimate.py
```

This script reads the data from either a CSV or YAML file (default is YAML) and calculates an estimated rating along with a 95% confidence interval.

### Customizing the Estimation
You can customize the estimation process by modifying the parameters in the `estimate.py` script:

- `initial_score`: The initial rating to start the estimation from (default: 1500), I recommend that you should set it to your contest rating.
- `learning_rate`: The learning rate for the gradient descent algorithm (default: 0.1).
- `max_iter`: The maximum number of iterations for the gradient descent algorithm (default: 1000).
- `decay_factor`: The decay factor for weighting recent samples more heavily (default: 0.99).

## Calculation Principle

The program uses a weighted ELO rating system to estimate the user's rating. The key steps in the calculation are as follows:

1. **Expected Score Calculation**: The expected score for each problem is calculated using the ELO formula:
   \[
   E = \frac{1}{1 + 10^{\frac{(R_{\text{problem}} - R_{\text{user}})}{400}}}
   \]
   where \( R_{\text{problem}} \) is the problem's rating and \( R_{\text{user}} \) is the user's current estimated rating.

2. **Weighted Gradient Descent**: The program uses a weighted gradient descent algorithm to iteratively update the user's rating. The weights are calculated based on the order of the samples, with more recent samples having higher weights. The weight for each sample is calculated as:
   \[
   w_i = \text{decay\_factor}^{N - i}
   \]
   where \( N \) is the total number of samples and \( i \) is the index of the sample.

3. **Confidence Interval Calculation**: After the final iteration, the program calculates a 95% confidence interval for the estimated rating. The confidence interval is calculated using the weighted standard error of the estimates.

## File Structure

- `src/`: Contains the main scripts for generating data and estimating ratings.
  - `data_generator.py`: Generates random test data in CSV and YAML formats.
  - `estimate.py`: Estimates the user's LeetCode rating based on the generated data.
- `tests/`: Contains test scripts.
- `data/`: Contains data files.
