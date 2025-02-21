import os
import pandas as pd

# Specify the directory containing the CSV files
directory = r'C:\MyPythonProjects\separated_unit'  # Replace with your directory path

# Initialize a set to store unique unit values
unique_units = set()

# Loop over all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {file_path}")
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        # Check if 'unit' column exists
        if 'unit' in df.columns:
            # Drop NaN values and get unique units
            units = df['unit'].dropna().unique()
            # Add unique units to the set
            unique_units.update(units)
        else:
            print(f"'unit' column not found in {filename}. Skipping this file.")
            continue

# Convert the set to a sorted list
unique_units = sorted(unique_units)

# Count the number of unique units
count = len(unique_units)

# Print the results
print(f"\nNumber of unique units: {count}\n")
print("List of unique units:")
for unit in unique_units:
    print(unit)
