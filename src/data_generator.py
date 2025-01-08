import random
import csv
import yaml


def generate_random_data_csv(num_samples=100, filename='./data/test_data.csv'):
    """Generate random question data and save to CSV file.
    
    Args:
        num_samples (int): Number of samples to generate
        filename (str): Path to save the CSV file
    """
    data = []
    for _ in range(num_samples):
        # Generate random question score between 1300 and 1900
        score = random.randint(1300, 1900)
        # Randomly determine if question was passed
        passed_flag = random.choice([True, False])
        data.append((score, passed_flag))

    # Save data to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write CSV header
        writer.writerow(['Score', 'Passed'])
        writer.writerows(data)
    print(f"Data saved to {filename}")


def generate_random_data_yaml(num_samples=100, filename='./data/test_data.yaml'):
    """Generate random question data and save to YAML file.
    
    Args:
        num_samples (int): Number of samples to generate
        filename (str): Path to save the YAML file
    """
    data = []
    for _ in range(num_samples):
        # Generate random question score between 1300 and 1900
        score = random.randint(1300, 1900)
        # Randomly determine if question was passed
        passed_flag = random.choice([True, False])
        data.append({
            'topic_score': score,
            'passed': passed_flag
        })

    # Create YAML structure
    yaml_data = {
        'data': data
    }

    # Save data to YAML file
    with open(filename, mode='w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    # Generate both CSV and YAML data
    # generate_random_data_csv()
    generate_random_data_yaml()