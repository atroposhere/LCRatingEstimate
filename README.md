# LeetCode Rating Estimate Tool

[中文版](./doc/README_ch.md)

This project is designed to help LeetCode users estimate their rating based on their recent problem-solving performance. The program uses the **Glicko-2 rating system** to calculate an estimated rating and provides a 95% confidence interval for the estimate.

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
    - `problem_rating`: The problem's rating (an integer between 1300 and 1900).
    - `passed`: A boolean value (`true` or `false`) indicating whether you passed the problem.

Example:
```yaml
data:
  - problem_rating: 1500
    passed: true
  - problem_rating: 1600
    passed: false
  - problem_rating: 1400
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
- `DATA_FILE`: The path to the data file (default: `./data/questions_data.yaml`).
- `USE_GLICKO`: A flag to decide whether to use the Glicko-2 system (default: `True`). If set to `False`, the legacy WGD method will be used (not recommended).

## Calculation Principle

### Glicko-2 Rating System
The Glicko-2 system is an advanced rating system that improves upon traditional ELO by incorporating **rating deviation (RD)** and **volatility**. These factors allow the system to better handle uncertainty and provide more accurate estimates over time.

1. **Rating and Rating Deviation**: Each user has a rating (μ) and a rating deviation (φ), which represents the uncertainty in their rating. A lower RD indicates higher confidence in the rating.

2. **Volatility**: This measures how much a user's rating fluctuates over time. High volatility suggests that the user's performance is inconsistent.

3. **Expected Outcome**: The expected outcome between two players (or a user and a problem) is calculated using a logistic function that considers both ratings and their deviations.

4. **Rating Update**: After each problem attempt, the user's rating, RD, and volatility are updated based on the outcome. The system uses an iterative algorithm to ensure that the updates are statistically sound.

5. **Confidence Interval**: The 95% confidence interval is calculated using the updated rating and RD, providing a range within which the user's true rating is likely to fall.

### Weighted Gradient Descent (WGD) Method
The WGD method is a legacy approach that uses a weighted gradient descent algorithm to estimate ratings. It incorporates a decay factor to prioritize recent data. But it encounted problems because of the sparse data. As such, it is not recommended for use.

## File Structure

- `src/`: Contains the main scripts for generating data and estimating ratings.
  - `data_generator.py`: Generates random test data in CSV and YAML formats.
  - `glicko_estimate.py`: Implements the Glicko-2 rating system.
  - `wgd_estimate.py`: Implements the deprecated WGD method.
  - `main.py`: The main script to run the estimation process.
- `tests/`: Contains test scripts.
- `data/`: Contains data files.