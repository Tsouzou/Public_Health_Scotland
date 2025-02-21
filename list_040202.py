import os
import pandas as pd

# Directory containing the CSV files
input_directory = r'C:\MyPythonProjects\separated_unit'  # Replace with your actual directory path

# Initialize a set to store unique BNFItemDescription entries
unique_descriptions = set()

# Loop over all CSV files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        # Check if required columns exist
        required_columns = ['BNFItemCode', 'BNFItemDescription']
        if not all(col in df.columns for col in required_columns):
            print(f"Missing required columns in {filename}. Skipping this file.")
            continue

        # Filter rows where BNFItemCode starts with '040202'
        filtered_df = df[df['BNFItemCode'].astype(str).str.startswith('040202')]

        if not filtered_df.empty:
            # Add unique BNFItemDescription entries to the set
            descriptions = filtered_df['BNFItemDescription'].dropna().unique()
            unique_descriptions.update(descriptions)
        else:
            print(f"No entries with BNFItemCode starting with '040202' in {filename}.")

# Convert the set to a sorted list
unique_descriptions = sorted(unique_descriptions)

# Print the results
print(f"\nNumber of unique BNFItemDescription entries with BNFItemCode starting with '040202': {len(unique_descriptions)}\n")
print("List of unique BNFItemDescription entries:")
for desc in unique_descriptions:
    print(desc)
