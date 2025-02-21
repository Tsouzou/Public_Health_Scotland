import pandas as pd

# Define the path to your CSV file
csv_file_path = r'C:\MyPythonProjects\sample\pitc202411.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Get the unique entries under 'GPPractice'
unique_gp_practices = df['GPPractice'].unique()

# Count the number of unique entries
num_unique_gp_practices = len(unique_gp_practices)

# Print the number of unique GPPractices
print(f"Number of unique GPPractices: {num_unique_gp_practices}\n")

# List all unique GPPractices
print("List of unique GPPractices:")
for gp in unique_gp_practices:
    print(gp)
