import os
import pandas as pd

# Directory containing the CSV files
directory = r'C:\MyPythonProjects\separated_unit'

# Initialize a set to store unique BNFItemDescription values
unique_descriptions = set()

# Loop over all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        # Read the CSV file
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        # Check if 'GPPractice' and 'BNFItemDescription' columns exist
        if 'GPPractice' not in df.columns or 'BNFItemDescription' not in df.columns:
            print(f"Required columns not found in {filename}. Skipping this file.")
            continue
        
        # Filter for GPPractice == 80005
        df_80005 = df[df['GPPractice'] == 80005]
        if not df_80005.empty:
            # Add unique BNFItemDescription values to the set
            unique_descriptions.update(df_80005['BNFItemDescription'].unique())
        else:
            print(f"No data for GPPractice 80005 in {filename}.")

# Convert the set to a sorted list
unique_descriptions = sorted(unique_descriptions)

# Count the number of unique BNFItemDescription values
count = len(unique_descriptions)

# Print the results
print(f"Number of unique BNFItemDescription for GPPractice 80005: {count}\n")
print("List of unique BNFItemDescription:")
for desc in unique_descriptions:
    print(desc)
