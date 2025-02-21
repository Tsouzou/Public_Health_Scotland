import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing the CSV files
input_directory = r'C:\MyPythonProjects\separated_unit'

# Base directory to save the plots
output_base_directory = r'C:\MyPythonProjects\Plots'

# Create the base output directory if it doesn't exist
if not os.path.exists(output_base_directory):
    os.makedirs(output_base_directory)

# Initialize an empty list to store dataframes
df_list = []

# Loop over all CSV files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)
        # Read the CSV file
        try:
            df = pd.read_csv(file_path)
            # Check if 'PaidDateMonth' column exists
            if 'PaidDateMonth' in df.columns:
                # Convert 'PaidDateMonth' to datetime
                df['PaidDateMonth'] = pd.to_datetime(df['PaidDateMonth'], format='%Y%m')
            else:
                print(f"'PaidDateMonth' column not found in {filename}. Skipping this file.")
                continue
            # Append to list
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

# Combine all dataframes into one
if df_list:
    data = pd.concat(df_list, ignore_index=True)
else:
    print("No data found in the directory.")
    exit()

# Ensure 'PaidQuantity' is numeric
data['PaidQuantity'] = pd.to_numeric(data['PaidQuantity'], errors='coerce')

# Drop rows with NaN in 'PaidQuantity'
data = data.dropna(subset=['PaidQuantity'])

# Ensure 'PaidDateMonth' is datetime
if data['PaidDateMonth'].dtype != 'datetime64[ns]':
    data['PaidDateMonth'] = pd.to_datetime(data['PaidDateMonth'], format='%Y%m')

# Sort data by 'PaidDateMonth'
data = data.sort_values('PaidDateMonth')

# Get unique GPPractices
gp_practices = data['GPPractice'].unique()

# For each GPPractice
for gp in gp_practices:
    print(f"Processing GPPractice {gp}")
    gp_data = data[data['GPPractice'] == gp]
    if gp_data.empty:
        print(f"No data for GPPractice {gp}.")
        continue
    # Create a folder for this GPPractice
    gp_output_directory = os.path.join(output_base_directory, str(gp))
    if not os.path.exists(gp_output_directory):
        os.makedirs(gp_output_directory)
    # Create a complete date range from the earliest to the latest month for this GPPractice
    all_months = pd.date_range(start=gp_data['PaidDateMonth'].min(), end=gp_data['PaidDateMonth'].max(), freq='MS')
    # Get unique BNFItemDescriptions
    bnf_descriptions = gp_data['BNFItemDescription'].unique()
    # Generate plots for each BNFItemDescription
    for description in bnf_descriptions:
        desc_data = gp_data[gp_data['BNFItemDescription'] == description]
        # Get unique units for this BNFItemDescription
        units = desc_data['unit'].unique()
        
        plt.figure(figsize=(12, 6))
        
        # Plot lines for each unit
        for unit in units:
            unit_data = desc_data[desc_data['unit'] == unit]
            # Aggregate data by 'PaidDateMonth'
            unit_data = unit_data.groupby('PaidDateMonth').agg({'PaidQuantity': 'sum'}).reset_index()
            # Set 'PaidDateMonth' as index
            unit_data = unit_data.set_index('PaidDateMonth')
            # Reindex to include all months, fill missing 'PaidQuantity' with 0
            unit_data = unit_data.reindex(all_months, fill_value=0)
            # Set the index name explicitly
            unit_data.index.name = 'PaidDateMonth'
            # Reset index to have 'PaidDateMonth' as a column
            unit_data = unit_data.reset_index()
            # Ensure data is sorted by 'PaidDateMonth'
            unit_data = unit_data.sort_values('PaidDateMonth')
            plt.plot(unit_data['PaidDateMonth'], unit_data['PaidQuantity'], label=unit)
        
        plt.title(f'PaidQuantity over Time for GPPractice {gp}\nBNFItemDescription: {description}')
        plt.xlabel('PaidDateMonth')
        plt.ylabel('PaidQuantity')
        plt.legend(title='Unit')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot to the GPPractice directory
        # Sanitize the filename by replacing forbidden characters
        safe_description = ''.join(c for c in description if c.isalnum() or c in (' ', '_')).rstrip()
        plot_filename = os.path.join(gp_output_directory, f"{safe_description}.png")
        plt.savefig(plot_filename)
        plt.close()  # Close the figure to free memory
    
        print(f"Plot saved for GPPractice '{gp}', BNFItemDescription '{description}' as '{plot_filename}'")
