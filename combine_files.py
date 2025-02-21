import os
import pandas as pd

# Specify the directory containing the CSV files
input_directory = r'C:\MyPythonProjects\separated_unit'  # Replace with your actual directory path

# Initialize a list to store DataFrames
df_list = []

# Loop over all files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)
        print(f"Processing file: {file_path}")
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

# Combine all DataFrames into one
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)
    print(f"\nCombined {len(df_list)} files into a single DataFrame.")
else:
    print("No CSV files found in the directory.")
    combined_df = pd.DataFrame()

# Save the combined DataFrame to a new CSV file
output_file = os.path.join(input_directory, 'combined_data.csv')
combined_df.to_csv(output_file, index=False)
print(f"\nCombined data saved to: {output_file}")
