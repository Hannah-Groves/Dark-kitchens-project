### FIELD VALIDATION AND DARK KITCHEN STATUS ###

# Install and import necessary packages
import pandas as pd
import webbrowser
import urllib.parse

# This function opens the street view in Google Maps of the address at input
def open_street_view_directly(address):
    """Open Google Maps Street View for the given address in the default web browser."""
    encoded_address = urllib.parse.quote(address)
    url = f"https://www.google.com/maps/place/{encoded_address}/&output=svembed"
    try:
        webbrowser.open(url, new=2)
        return True
    except Exception as e:
        print(f"Error opening URL: {e}")
        return False

# This function relies on manual input for dark kitchen status
def verify_dark_kitchens(csv_path):
    df = pd.read_csv(csv_path)

    # Start a new column to save the dark kitchen status of each establishment
    df['Is Dark Kitchen'] = pd.NA

    # Loop through the establishments
    for index, row in df.iterrows():
        address = row['Address']
        name = row['Restaurant Name']
        print(f"Processing: {name} at {address}")
        
        success = open_street_view_directly(address)
        
        if not success:
            # Some addresses may not be in correct format, here we have the option to correct if possible
            new_address = input("Failed to open the address in Google Maps. Please enter a corrected address or type 'skip' to skip this entry: ")
            if new_address.lower() == 'skip':
                continue 
            else:
                row['Address'] = new_address
                success = open_street_view_directly(new_address) 
                if not success:
                    print("Still unable to open the address. Moving to the next entry.")
                    continue
        
        # Proceed if the address was successfully opened and prompt user to determine dark kitchen status
        user_input = input("Is this a dark kitchen? (T/F/Skip): ").lower()
        if user_input == 't':
            df.at[index, 'Is Dark Kitchen'] = True
        elif user_input == 'f':
            df.at[index, 'Is Dark Kitchen'] = False
        elif user_input == 'skip':
            continue

    # Save entered data to CSV file  
    updated_csv = csv_path.replace('.csv', '_verified.csv')
    df.to_csv(updated_csv, index=False)
    print(f"Updated data saved to {updated_csv}")

# Insert here the path to the relevant CSV file (must contain the addresses)
csv_path = r'C:\Users\location1_fsa.csv'
verify_dark_kitchens(csv_path)
