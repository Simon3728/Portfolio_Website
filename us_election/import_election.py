"""
Script to process and import election data into the Django database.

This script reads election data from text files, processes the data, and inserts it into the database 
using the ElectionResult model from the us_election application.
"""

import os
import django
import sys
import pandas as pd
import re

# Set up Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

from us_election.models import ElectionResult

# Dictionary for mapping state abbreviations to state names
state_names = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
    'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

def main():
    """
    Main function to process election data files and insert the data into the database.
    """
    file_paths = [
        'president_2000.txt', 'president_2004.txt', 
        'president_2008.txt', 'president_2012.txt', 
        'president_2016.txt', 'president_2020.txt'
    ]

    # Process each file and combine the data
    all_data = pd.DataFrame()
    for file_name in file_paths:
        file_path = os.path.join(BASE_DIR, 'us_election', 'Data_Files', 'Election', file_name)
        data_percentage = read_and_process_file(file_path)
        all_data = pd.concat([all_data, data_percentage], ignore_index=True)
    
    # Insert all data into the database using Django models
    insert_data_to_db(all_data)

def read_and_process_file(file_path):
    """
    Read and process an election data file.
    """
    # Extract year from filename
    year_match = re.search(r'president_(\d{4})\.txt', file_path)
    year = int(year_match.group(1)) if year_match else None

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return pd.DataFrame()

    # Extract the header and data
    header = lines[0].strip().split()
    data = [line.strip().split() for line in lines[1:]]

    # Map the header to expected columns
    column_mapping = {
        'State': 'StateCode',
        'Republican': 'Republican',
        'Democratic': 'Democratic',
        'Others': 'Others',
        'Total': 'Total'
    }

    # Ensure the header columns are in the expected order
    columns = [column_mapping[col] for col in header if col in column_mapping]

    df = pd.DataFrame(data, columns=columns)

    # Clean numeric data by removing commas
    numeric_columns = ['Republican', 'Democratic', 'Others', 'Total']
    for column in numeric_columns:
        df[column] = df[column].str.replace(',', '').astype(float)

    # Add the 'Year' column and map state names
    df['Year'] = year
    df['State'] = df['StateCode'].map(state_names)

    return df[['State', 'Year', 'Republican', 'Democratic', 'Others', 'Total']]

def insert_data_to_db(data):
    """
    Insert the processed data into the database using Django ORM.
    """
    for _, row in data.iterrows():
        ElectionResult.objects.create(
            state=row['State'],
            year=row['Year'],
            republican=row['Republican'],
            democratic=row['Democratic'],
            others=row['Others'],
            total=row['Total']
        )

if __name__ == '__main__':
    main()
