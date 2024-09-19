### COMBINE DATA FROM ALL FOOD DELIVERY WEBSITES ###

# Install and import necessary packages
import pandas as pd
from fuzzywuzzy import fuzz

# Load datasets from Just Eat and Deliveroo (include here the path to the corresponding datasets on your device)
justeat_df = pd.read_csv(r'C:\Users\justeat_location1.csv')
deliveroo_df = pd.read_csv(r'C:\Users\deliveroo_location1.csv')

# This function cleans and prepares names for deduplication
def clean_name(name):
    name = name.lower()
    name = ''.join(e for e in name if e.isalnum())
    return name

# Apply cleaning function to each dataset
justeat_df['Clean Name'] = justeat_df['Restaurant Name'].apply(clean_name)
deliveroo_df['Clean Name'] = deliveroo_df['Restaurant Name'].apply(clean_name)

# Combine the dataframes with no duplicates
combined_df = pd.DataFrame(columns=justeat_df.columns[:-1])

seen_names = set()

for _, row in justeat_df.iterrows():
    combined_df = pd.concat([combined_df, pd.DataFrame([row.drop('Clean Name')])], ignore_index=True)
    seen_names.add(row['Clean Name'])

for _, row in deliveroo_df.iterrows():
    if row['Clean Name'] not in seen_names:
        
        # Check for partial matches with a high similarity threshold
        is_duplicate = False
        for name in seen_names:
            if fuzz.partial_ratio(name, row['Clean Name']) > 90:
                is_duplicate = True
                break
        if not is_duplicate:
            combined_df = pd.concat([combined_df, pd.DataFrame([row.drop('Clean Name')])], ignore_index=True)

# Save the combined data to a new CSV file
combined_df.to_csv('combined_location1.csv', index=False)
print("Combined CSV has been saved.")
