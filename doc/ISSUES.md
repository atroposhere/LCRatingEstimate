# Issue Tracking

## Known Issues

### Rating Convergence Issue
- **Description**: When adding 100 records of passing 1700-rated problems, the rating does not show a trend converging to 1700.
- **Severity**: Medium
- **Category**: Algorithm Accuracy
- **Related Components**: 
  - `src/glicko_estimate.py` (Glicko-2 implementation)
  - `src/main.py` (Rating calculation)
- **Expected Behavior**: The rating should gradually converge towards the target rating (1700) as more successful attempts are recorded.
- **Current Behavior**: The rating remains unstable and does not show expected convergence.
- **Reproduction Steps**:
  1. Generate test data with 100 records of passed 1700-rated problems
  2. Run rating estimation using `main.py`
  3. Observe the rating trend over iterations