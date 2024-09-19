### CROSS-REFERENCE DATA WITH FSA ###

# Install and import necessary packages
import xml.etree.ElementTree as ET
import pandas as pd

# Insert here the path to the corresponding downloaded FSA data
tree_location1 = ET.parse(r'C:\Users\Location1 FSA data.xml')
root_location1 = tree_location1.getroot()

# Extract establishment details
fsa_data = []
for est in root_location1.findall('.//EstablishmentDetail'):
    name = est.find('./BusinessName').text if est.find('./BusinessName') is not None else ""
    address_lines = [
        est.find('./AddressLine1').text if est.find('./AddressLine1') is not None else "",
        est.find('./AddressLine2').text if est.find('./AddressLine2') is not None else "",
        est.find('./AddressLine3').text if est.find('./AddressLine3') is not None else "",
        est.find('./AddressLine4').text if est.find('./AddressLine4') is not None else "",
        est.find('./PostCode').text if est.find('./PostCode') is not None else ""
    ]
    address = ", ".join(filter(None, address_lines))
    fsa_data.append({'Name': name.strip(), 'Address': address.strip()})

# Convert the data from a list to a dataframe
fsa_df = pd.DataFrame(fsa_data)

# Display the first entries of the FSA data to inspect
print(fsa_df.head())

# Insert the path to the combined Just Eat and Deliveroo dataset on your device
combined_location1_df = pd.read_csv(r'C:\Users\combined_location1.csv')

# Clean names for cross-referencing
combined_location1_df['Clean Name'] = combined_location1_df['Restaurant Name'].apply(lambda x: x.lower().strip())
fsa_df['Clean Name'] = fsa_df['Name'].apply(lambda x: x.lower().strip())

# Start column for documenting FSA registration of each establishment
combined_location1_df['In FSA Data'] = False

# Loop through the entries and check registration
for index, row in combined_location1_df.iterrows():
    restaurant_name = row['Clean Name']
    
    # Update 'In FSA Data' column if restaurant name found in FSA data
    if any(fsa_df['Clean Name'].str.contains(restaurant_name)):
        combined_location1_df.at[index, 'In FSA Data'] = True

# Save the updated dataframe to a CSV file
combined_location1_df.to_csv(r'C:\Users\location1_with_fsa.csv', index=False)
print("Updated CSV with FSA data check has been saved.")
