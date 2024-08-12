"""
This script reads election data from a CSV file, processes it, and inserts it into the Django database. 
It includes functions to read and process the CSV file, insert the data into the database, and verify the insertion.
"""

import os
import sys
import django
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

from us_election.models import PopulationData

def main():
    file_path = os.path.join(BASE_DIR, 'us_election', 'Data_Files', 'age_sex_data.csv')
    data = read_and_process_file(file_path)
    if not data.empty:
        insert_data_to_db(data)

def read_and_process_file(file_path):
    """Read and process the CSV file, returning a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        state_data = data[(data['Countyfips'] == 0) & (data['Statefips'] != 0)]
        return state_data
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return pd.DataFrame()  

def insert_data_to_db(data):
    """Insert the processed data into the Django database."""
    population_data_objects = [
        PopulationData(
            name=row['Description'],
            year=row['Year'],
            total_population=row['Total Population'],
            population_0_4=row['Population 0-4'],
            population_5_17=row['Population 5-17'],
            population_18_24=row['Population 18-24'],
            population_25_44=row['Population 25-44'],
            population_45_64=row['Population 45-64'],
            population_65_plus=row['Population 65+'],
            population_under_18=row['Population Under 18'],
            population_18_54=row['Population 18-54'],
            population_55_plus=row['Population 55+'],
            male_population=row['Male Population'],
            female_population=row['Female Population']
        )
        for _, row in data.iterrows()
    ]

    try:
        PopulationData.objects.bulk_create(population_data_objects)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data into the database: {e}")

if __name__ == '__main__':
    main()
