"""
Script to verify and validate population data from the Django database.

This script checks for data integrity by verifying the sum of population age groups,
gender population consistency, and the presence of NULL or NaN values.
"""

import os
import django
import sys
import math

# Set up Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

from us_election.models import PopulationData

def main():
    tolerance = 0.005  # 0.5% tolerance for numerical comparisons
    rows = fetch_population_data()
    critical_entries = validate_population_data(rows, tolerance)
    null_entries = check_for_null_values(rows)

    # Print critical entries found during validation
    for entry in critical_entries:
        print(f"Critical Entry - ID: {entry[0]}, Name: {entry[1]}, Year: {entry[2]}, Issue: {entry[3]}")

    # Print entries with NULL or NaN values
    for entry in null_entries:
        print(f"Null Value Entry - ID: {entry[0]}, Name: {entry[1]}, Year: {entry[2]}, Issue: {entry[3]}")

def roughly_equal(a, b, tolerance):
    """
    Check if two values are roughly equal within a given tolerance.
    """
    return abs(a - b) <= tolerance * max(a, b)

def fetch_population_data():
    """
    Fetch population data from the Django database.
    """
    results = PopulationData.objects.all().values_list(
        'id', 'name', 'year', 'total_population',
        'population_0_4', 'population_5_17', 'population_18_24',
        'population_25_44', 'population_45_64', 'population_65_plus',
        'male_population', 'female_population'
    )
    return list(results)

def validate_population_data(rows, tolerance):
    """
    Validate the population data to check for mismatches in age groups sum and gender population.
    """
    critical_entries = []

    for row in rows:
        id, name, year, total_population, population_0_4, population_5_17, population_18_24, \
        population_25_44, population_45_64, population_65_plus, male_population, female_population = row

        # Calculate the sum of the age groups
        age_groups_sum = (population_0_4 + population_5_17 + population_18_24 +
                          population_25_44 + population_45_64 + population_65_plus)

        # Check if age groups sum roughly equals total_population
        if not roughly_equal(age_groups_sum, total_population, tolerance):
            critical_entries.append((id, name, year, f'Age groups sum mismatch: calculated sum={age_groups_sum}, total_population={total_population}'))

        # Check if male_population + female_population equals total_population
        if not roughly_equal(male_population + female_population, total_population, tolerance):
            critical_entries.append((id, name, year, f'Gender population mismatch: male_population={male_population}, female_population={female_population}, total_population={total_population}'))

    return critical_entries

def check_for_null_values(rows):
    """
    Check for NULL and NaN values in the population data entries.
    """
    null_entries = []

    for row in rows:
        if any(col is None or (isinstance(col, float) and math.isnan(col)) for col in row):
            null_entries.append((row[0], row[1], row[2], 'NULL or NaN values found in entry'))

    return null_entries

if __name__ == "__main__":
    main()
