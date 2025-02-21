import pandas as pd
import re

# Define postcode districts for each damage level
damage_levels = {
    'No or Minimal': [
        # Western Isles
        'HS1', 'HS2', 'HS3', 'HS4', 'HS6', 'HS7', 'HS8', 'HS9', 'HS10', 'HS11',
        # Isle of Skye
        'IV56', 'IV57',
        # Highland West Coast
        'IV1', 'IV2', 'IV3', 'IV4', 'IV5', 'IV21', 'IV22', 'IV23', 'IV24', 'IV25',
        # Argyll & Bute
        'PA20', 'PA21', 'PA22', 'PA23', 'PA24', 'PA25', 'PA26', 'PA27', 'PA28', 'PA29',
        # Dumfries & Galloway
        'DG1', 'DG2', 'DG3', 'DG4', 'DG5', 'DG6', 'DG7', 'DG8', 'DG9'
    ],
    'Less or Moderate': [
        # Lothians
        'EH1', 'EH2', 'EH3', 'EH4', 'EH5', 'EH6', 'EH7', 'EH8', 'EH9', 'EH10', 'EH11', 'EH12', 'EH14',
        # Fife
        'KY1', 'KY2', 'KY3', 'KY4', 'KY5', 'KY6', 'KY7', 'KY8', 'KY9', 'KY10', 'KY11', 'KY12', 'KY13', 'KY14',
        # Perth & Kinross
        'PH1', 'PH2', 'PH3', 'PH4', 'PH5', 'PH6', 'PH7', 'PH8', 'PH9', 'PH10'
    ],
    'Most': [
        # Aberdeenshire
        'AB10', 'AB11', 'AB12', 'AB13', 'AB14', 'AB15', 'AB16', 'AB21', 'AB22', 'AB23', 'AB24', 'AB25',
        'AB30', 'AB31', 'AB32', 'AB33', 'AB34', 'AB35', 'AB36', 'AB37', 'AB38', 'AB39', 'AB42', 'AB43',
        'AB44', 'AB45',
        # Moray
        'IV30', 'IV31', 'IV32', 'IV33', 'IV34', 'IV35', 'IV36', 'IV37', 'IV38', 'IV39', 'IV40', 'IV41',
        # Angus
        'DD1', 'DD2', 'DD3', 'DD4', 'DD5', 'DD6', 'DD7', 'DD8', 'DD9',
        # Eastern Tayside
        'TD1', 'TD2', 'TD3', 'TD4', 'TD5', 'TD6', 'TD7', 'TD8', 'TD9', 'TD10', 'TD11', 'TD12', 'TD13',
        # North-East Highlands & Easter Ross
        'IV19', 'IV20'
    ]
}

# Create a district to damage level mapping for quick lookup
district_damage_level = {}
for level, districts in damage_levels.items():
    for district in districts:
        district_damage_level[district] = level

# Function to determine if input is a postcode area or district
def determine_input_type(postcode_input):
    if re.match(r'^[A-Z]{1,2}$', postcode_input):
        return 'area'
    elif re.match(r'^[A-Z]{1,2}\d{1,2}$', postcode_input):
        return 'district'
    else:
        return 'invalid'

def main():
    # Prompt the user to enter the postcode district or area
    user_input = input("Enter the postcode district or area (e.g., 'AB10' or 'HS'): ").strip().upper()

    # Determine the type of input
    input_type = determine_input_type(user_input)

    if input_type == 'invalid':
        print("Invalid postcode format. Please enter a valid outward code (e.g., 'AB10' or 'HS').")
        return

    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv('GP_Practices_Scotland.csv')
    except FileNotFoundError:
        print("Error: The file 'GP_Practices_Scotland.csv' was not found.")
        return
    except pd.errors.EmptyDataError:
        print("Error: The file 'GP_Practices_Scotland.csv' is empty.")
        return
    except pd.errors.ParserError:
        print("Error: The file 'GP_Practices_Scotland.csv' is corrupted or has an incorrect format.")
        return

    # Check if 'postcode' and 'prac_code' columns exist
    required_columns = {'postcode', 'prac_code'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        print(f"Error: Missing columns in CSV file: {', '.join(missing)}")
        return

    # Extract the outward code from the 'postcode' column
    # This assumes that the postcode is in the standard format, e.g., 'AB10 1AA'
    df['outward_code'] = df['postcode'].str.extract(r'^([A-Z]{1,2}\d{1,2})', expand=False).str.upper()

    if input_type == 'area':
        # For postcode area, filter all districts starting with the area initial
        df_filtered = df[df['outward_code'].str.startswith(user_input, na=False)]
        
        # Get unique districts in this area
        matched_districts = df_filtered['outward_code'].unique()
        
        # Initialize a dictionary to hold practice codes per damage level
        damage_level_prac_codes = {}
        for district in matched_districts:
            level = district_damage_level.get(district, "Unknown")
            if level not in damage_level_prac_codes:
                damage_level_prac_codes[level] = []
            # Get practice codes for this district
            codes = df_filtered[df_filtered['outward_code'] == district]['prac_code'].dropna().tolist()
            damage_level_prac_codes[level].extend(codes)
        
        # Remove 'Unknown' if present and empty
        if "Unknown" in damage_level_prac_codes and not damage_level_prac_codes["Unknown"]:
            del damage_level_prac_codes["Unknown"]
        
        # Check if any records match the filter
        if not damage_level_prac_codes:
            print(f"No records found with postcode area '{user_input}'.")
        else:
            print(f"\nPractice Codes in postcode area '{user_input}' grouped by Damage Levels:")
            for level, codes in damage_level_prac_codes.items():
                if codes:
                    print(f"\n**{level}**")
                    print(" ".join(map(str, codes)))
    
    elif input_type == 'district':
        # For postcode district, filter where outward_code matches exactly
        df_filtered = df[df['outward_code'] == user_input]
        damage_level = district_damage_level.get(user_input, "Unknown")
        
        if damage_level == "Unknown":
            print(f"The postcode district '{user_input}' does not have an assigned damage level.")
            return
        
        # Check if any records match the filter
        if df_filtered.empty:
            print(f"No records found with postcode district '{user_input}'.")
        else:
            # Extract 'prac_code' entries and convert to a list
            prac_codes = df_filtered['prac_code'].dropna().tolist()

            if prac_codes:
                print(f"\nPractice Codes in postcode district '{user_input}' with Damage Level: **{damage_level}**")
                # Modify the output to be space-separated
                print(" ".join(map(str, prac_codes)))
            else:
                print(f"No 'prac_code' entries found for postcode district '{user_input}'.")

if __name__ == "__main__":
    main()
