import csv
import json

# Utility functions for the app
def read_csv(filepath):
    try:
        with open(filepath, mode='r') as infile:
            reader = csv.DictReader(infile)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def write_csv(filepath, data):
    with open(filepath, mode='w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Future utility for migrating to SQL
# def migrate_to_sql():
#     pass # Implement data migration logic here