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

### Data Preparation
To estimate your LeetCode rating, you need to prepare your problem-solving data and place it in the `/data` directory. The data should be in one of the following formats:

#### YAML Format
- File name: `questions_data.yaml`
- File location: `/data/questions_data.yaml`
- Data format:
  - The file should contain a list of dictionaries under the key `data`.
  - Each dictionary should have two keys:
    - `topic_score`: The problem's rating (an integer between 1300 and 1900).
    - `passed`: A boolean value (`true` or `false`) indicating whether you passed the problem.

Example:
```yaml
data:
  - topic_score: 1500
    passed: true
  - topic_score: 1600
    passed: false
  - topic_score: 1400
    passed: true
```

#### CSV Format
- File name: `questions_data.csv`
- File location: `/data/questions_data.csv`
- Data format:
  - Each row represents a problem you have attempted.
  - The first column is the problem's rating (an integer between 1300 and 1900).
  - The second column is a boolean value (`True` or `False`) indicating whether you passed the problem.

Example:
```
Score,Passed
1500,True
1600,False
1400,True
```



#### Generating Test Data
If you want to test the program before preparing your own data, you can generate random test data using the `data_generator.py` script. This script generates both CSV and YAML files containing random problem scores and pass/fail flags.

```bash
python src/data_generator.py
```

By default, the script generates 100 samples and saves them to `./data/test_data.csv` and `./data/test_data.yaml`.

### Estimating LeetCode Rating
To estimate your LeetCode rating based on the generated data, use the `main.py` script:

```bash
python src/main.py
```

This script reads the data from either a CSV or YAML file (default is YAML) and calculates an estimated rating along with a 95% confidence interval.

### Customizing the Estimation
You can customize the estimation process by modifying the parameters in the `main.py` script:

- `INITIAL_SCORE`: The initial rating to start the estimation from (default: 1580), I recommend that you should set it to your contest rating.
- `LEARNING_RATE`: The learning rate for the gradient descent algorithm (default: 0.1).
- `MAX_ITER`: The maximum number of iterations for the gradient descent algorithm (default: 2000).
- `DECAY_FACTOR`: The decay factor for weighting recent samples more heavily (default: 0.99).
- `DATA_FILE`: The path to the data file (default: `./data/questions_data.yaml`).

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
  - `estimate.py`: Contains the core logic for estimating the user's LeetCode rating.
  - `main.py`: The main script to run the estimation process.
- `tests/`: Contains test scripts.
- `data/`: Contains data files.