import os
import pandas as pd
import re

# Specify the directory containing the CSV files to process
input_directory = r'C:\MyPythonProjects\Output'  # Replace with your actual directory path

# Specify the directory where you want to save the modified files
output_directory = r'C:\MyPythonProjects\separated_unit'  # Replace with your desired output directory

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to split the text at the first occurrence of a digit
def split_at_first_digit(text):
    if pd.isna(text):
        return text, ''
    match = re.search(r'\d', text)
    if match:
        index = match.start()
        return text[:index].strip(), text[index:].strip()
    else:
        return text.strip(), ''

# Loop over all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(input_directory, filename)
        print(f"Processing file: {input_file_path}")
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_file_path)
        
        # Check if 'BNFItemDescription' column exists
        if 'BNFItemDescription' in df.columns:
            # Apply the splitting function
            split_results = df['BNFItemDescription'].apply(split_at_first_digit)
            split_df = pd.DataFrame(split_results.tolist(), columns=['BNFItemDescription', 'unit'], index=df.index)
            
            # Replace original 'BNFItemDescription' column with the split first part
            df['BNFItemDescription'] = split_df['BNFItemDescription']
            
            # Insert 'unit' column immediately after 'BNFItemDescription'
            col_idx = df.columns.get_loc('BNFItemDescription') + 1
            df.insert(col_idx, 'unit', split_df['unit'])
            
            # Save the modified DataFrame to the output directory with the original file name
            output_file_path = os.path.join(output_directory, filename)
            df.to_csv(output_file_path, index=False)
            
            print(f"File saved as: {output_file_path}\n")
        else:
            print(f"'BNFItemDescription' column not found in {filename}. Skipping this file.\n")
