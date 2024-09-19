This folder contains code written in Python for collecting and analysing data on dark kitchens in the UK using food delivery websites.

justeat.py - Collects data from Just Eat website and creates a csv file, you will need a Just Eat url for the particular location where you want to find food establishments
deliveroo.py - Collects data from Deliveroo website and creates a csv file, you will need a Deliveroo url for the particular location where you want to find food establishments
combine_data.py - Combines both datasets and removes duplicates
check_fsa.py - Checks for registration with Food Standards Agency (FSA), you will need to download the appropriate FSA data from their website to cross-reference
dark_kitchens_check.py - Speeds up manual process of field validation and identifying dark kitchens: for each address, this code will open Google Maps 360 degree view and will ask the reviewer to input "Y" or "N" for dark kitchens status. This code also helps correct any errors in addresses collected.
