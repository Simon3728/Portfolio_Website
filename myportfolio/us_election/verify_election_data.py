import os
import django
import sys
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

from us_election.models import ElectionResult

def main():
    tolerance = 0.0001 # 0.01%

    rows = fetch_election_data()

    critical_entries = validate_election_data(rows, tolerance)

    null_entries = check_for_null_values(rows)

    for entry in critical_entries:
        print(f"Critical Entry - ID: {entry[0]}, State: {entry[1]}, Year: {entry[2]}, Issue: {entry[3]}")

    for entry in null_entries:
        print(f"Null Value Entry - ID: {entry[0]}, State: {entry[1]}, Year: {entry[2]}, Issue: {entry[3]}")

def roughly_equal(a, b, tolerance):
    """
    Check if two values are roughly equal within a given tolerance.
    """
    return abs(a - b) <= tolerance * max(a, b)

def fetch_election_data():
    """
    Fetch election data from the Django database.
    """
    results = ElectionResult.objects.all().values_list('id', 'state', 'year', 'republican', 'democratic', 'others', 'total')
    return list(results)

def validate_election_data(rows, tolerance):
    """
    Validate the election data to check for mismatches in total votes.
    """
    critical_entries = []

    for row in rows:
        # Calculate the sum of the votes
        votes_sum = (row[3] + row[4] + row[5])
        # Check if age groups sum roughly equals total_population
        if not roughly_equal(votes_sum, row[6], tolerance):
            critical_entries.append((row[0], row[1], row[2], f'Votes sum mismatch: calculated sum={votes_sum}, total={row[6]}'))

    return critical_entries

def check_for_null_values(rows):
    """
    Check for NULL and NaN values in the election data entries.
    """
    null_entries = []

    for row in rows:
        if any(col is None or (isinstance(col, float) and math.isnan(col)) for col in row):
            null_entries.append((row[0], row[1], row[2], 'NULL or NaN values found in entry'))

    return null_entries

if __name__ == "__main__":
    main()