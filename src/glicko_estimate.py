"""
This module implements a Glicko-2 rating system for estimating LeetCode ratings.
The Glicko-2 system is an improvement over the ELO system, incorporating rating
volatility and providing more accurate estimates over time.
"""

import math
import csv
import yaml
import numpy as np

# Constants for Glicko-2 system
GLICKO2_Q = math.log(10) / 400
GLICKO2_PI_SQUARED = math.pi ** 2
MIN_RD = 30  # Minimum rating deviation for problems


def glicko2_scale_rating(rating):
    """Scale the rating to the Glicko-2 scale."""
    return (rating - 1500) / 173.7178


def glicko2_scale_rd(rd):
    """Scale the rating deviation to the Glicko-2 scale."""
    return rd / 173.7178


def glicko2_scale_back_rating(rating):
    """Scale the rating back to the original scale."""
    return rating * 173.7178 + 1500


def glicko2_scale_back_rd(rd):
    """Scale the rating deviation back to the original scale."""
    return rd * 173.7178


def glicko2_g(rd):
    """Calculate the Glicko-2 g function."""
    return 1 / math.sqrt(1 + 3 * (GLICKO2_Q ** 2) * (rd ** 2) / GLICKO2_PI_SQUARED)


def glicko2_e(rating, rating_j, rd_j):
    """Calculate the expected outcome between two players."""
    return 1 / (1 + math.exp(-glicko2_g(rd_j) * (rating - rating_j)))


def glicko2_update_rating(rating, rd, volatility, results, tau=0.5):
    """
    Update the rating using the Glicko-2 system.

    Args:
        rating (float): The current rating.
        rd (float): The current rating deviation.
        volatility (float): The current rating volatility.
        results (list): List of tuples (rating_j, rd_j, outcome).
        tau (float): The system constant that constrains the change in volatility.

    Returns:
        tuple: Updated rating, rating deviation, and volatility.
    """
    # Step 1: Convert to Glicko-2 scale
    mu = glicko2_scale_rating(rating)
    phi = glicko2_scale_rd(rd)

    # Step 2: Compute the variance and delta
    variance = 0
    delta = 0
    for rating_j, rd_j, outcome in results:
        mu_j = glicko2_scale_rating(rating_j)
        phi_j = glicko2_scale_rd(rd_j)
        g_phi_j = glicko2_g(phi_j)
        e = glicko2_e(mu, mu_j, phi_j)
        variance += (g_phi_j ** 2) * e * (1 - e)
        delta += g_phi_j * (outcome - e)

    variance = 1 / variance
    delta = delta * variance

    # Step 3: Determine the new volatility
    a = math.log(volatility ** 2)

    def f(x):
        ex = math.exp(x)
        num = ex * (delta ** 2 - phi ** 2 - variance - ex)
        den = 2 * (phi ** 2 + variance + ex) ** 2
        return (ex * (delta ** 2 - phi ** 2 - variance - ex)) / (2 * (phi ** 2 + variance + ex) ** 2) - (x - a) / (tau ** 2)

    # Use the Illinois algorithm to find the new volatility
    A = a
    if delta ** 2 > phi ** 2 + variance:
        B = math.log(delta ** 2 - phi ** 2 - variance)
    else:
        k = 1
        while f(a - k * tau) < 0:
            k += 1
        B = a - k * tau

    fA = f(A)
    fB = f(B)

    while abs(B - A) > 0.000001:
        C = A + (A - B) * fA / (fB - fA)
        fC = f(C)
        if fC * fB < 0:
            A = B
            fA = fB
        else:
            fA = fA / 2
        B = C
        fB = fC

    new_volatility = math.exp(A / 2)

    # Step 4: Update the rating deviation
    phi_star = math.sqrt(phi ** 2 + new_volatility ** 2)

    # Step 5: Update the rating and rating deviation
    new_phi = 1 / math.sqrt(1 / (phi_star ** 2) + 1 / variance)
    new_mu = mu + (new_phi ** 2) * delta

    # Step 6: Convert back to the original scale
    new_rating = glicko2_scale_back_rating(new_mu)
    new_rd = glicko2_scale_back_rd(new_phi)

    return new_rating, new_rd, new_volatility


def estimate_score_with_glicko(data, initial_score=1580, initial_rd=350, initial_volatility=0.06):
    """
    Estimate the LeetCode rating using the Glicko-2 system.

    Args:
        data (list): List of tuples (problem_rating, passed_flag).
        initial_score (float): The initial rating to start the estimation from.
        initial_rd (float): The initial rating deviation.
        initial_volatility (float): The initial rating volatility.

    Returns:
        tuple: Estimated score and 95% confidence interval.
    """
    rating = initial_score
    rd = initial_rd
    volatility = initial_volatility

    results = []
    for problem_rating, passed_flag in data:
        outcome = 1 if passed_flag else 0
        results.append((problem_rating, MIN_RD, outcome))

    new_rating, new_rd, new_volatility = glicko2_update_rating(
        rating, rd, volatility, results)

    # Calculate 95% confidence interval
    confidence_interval = (new_rating - 1.96 * new_rd,
                           new_rating + 1.96 * new_rd)

    return new_rating, confidence_interval


def read_data_from_csv(filename='./data/questions_data.csv'):
    """
    Read data from a CSV file.

    Args:
        filename (str): Path to the CSV file.

    Returns:
        list: List of tuples (problem_rating, passed_flag).
    """
    data = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            score = int(row[0])
            passed_flag = row[1] == 'True'
            data.append((score, passed_flag))
    return data


def read_data_from_yaml(filename='./data/questions_data.yaml'):
    """
    Read data from a YAML file.

    Args:
        filename (str): Path to the YAML file.

    Returns:
        list: List of tuples (problem_rating, passed_flag).
    """
    with open(filename, 'r') as f:
        raw_data = yaml.safe_load(f)
    data = [[item["problem_rating"], item["passed"]] for item in raw_data["data"]]
    return data
