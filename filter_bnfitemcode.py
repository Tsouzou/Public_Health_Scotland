import pandas as pd
import os

# Define the input and output directories
input_directory = r'C:\MyPythonProjects\Input'
output_directory = r'C:\MyPythonProjects\Output'
os.makedirs(output_directory, exist_ok=True)

# Set the chunk size (small due to limited RAM)
chunksize = 50000  # Adjust this value based on your system

# Loop over each CSV file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)

        # Initialize header_written flag
        header_written = False

        # Read and process the file in chunks
        for chunk in pd.read_csv(input_file_path, chunksize=chunksize, dtype={'BNFItemCode': str}):
            # Filter the chunk
            filtered_chunk = chunk[chunk['BNFItemCode'].str.startswith('0402', na=False)]

            # Write the filtered chunk to the output file
            if not filtered_chunk.empty:
                filtered_chunk.to_csv(output_file_path, mode='a', index=False, header=not header_written)
                header_written = True

        if not header_written:
            print(f"No matching rows found in {filename}")
        else:
            print(f"Filtered data saved to {output_file_path}")
