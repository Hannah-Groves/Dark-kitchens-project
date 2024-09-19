### SCRAPING DATA FROM DELIVEROO WEBSITE ###

# Install and import necessary packages
import csv
import time
import re 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# This function is used to extract the correct numbers when dealing with decimals
def extract_floats(text):
    """Extract floating-point numbers from strings."""
    matches = re.findall(r"\d+\.\d+|\d+", text) 
    return matches[0] if matches else 'N/A'

# This function takes the given URL and scrapes the necessary data
def scrape_deliveroo(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Create CSV file with necessary columns
    with open('deliveroo_location1.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Restaurant Name', 'Distance (miles)', 'Min Delivery Time (mins)', 
                         'Max Delivery Time (mins)', 'Diff Min-Max Delivery Time (mins)',
                         'Rating', 'Number of Reviews'])

        # Make a list of all establishments on Deliveroo website
        restaurants = soup.find_all('div', class_="HomeFeedUICard-cdbc09faf7465d96")
        
        # Loop through the establishments and collect necessary data
        for restaurant in restaurants:
            aria_label = restaurant.find('a').get('aria-label', '')
            print(aria_label)  # Debugging line

            # Find name of extablishment
            name = aria_label.split('.')[0]
            distance_part = aria_label.split('.')[1] if len(aria_label.split('.')) > 1 else 'N/A'
            distance = extract_floats(distance_part)

            # Find delivery times
            time_info = aria_label.split('Delivers in ')[1].split('.')[0] if 'Delivers in ' in aria_label else '0-0'
            delivery_times = [s for s in time_info.split(' to ')]
            min_time = extract_floats(delivery_times[0])
            max_time = extract_floats(delivery_times[1]) if len(delivery_times) > 1 else min_time
            time_diff = str(int(float(max_time)) - int(float(min_time))) if min_time and max_time else 'N/A'

            # Find delivery fees
            cost_section = aria_label.split('£')[1] if '£' in aria_label else '0'
            delivery_cost = extract_floats(cost_section.split(' delivery')[0])

            # Find star rating
            rating_section = aria_label.split('Rated ')[1] if 'Rated ' in aria_label else '0'
            rating = extract_floats(rating_section.split(' from')[0])

            # Find number of reviews
            review_section = aria_label.split('from ')[1] if 'from ' in aria_label else '0'
            reviews = extract_floats(review_section.split(' reviews')[0])

            # Include all extracted data into CSV file
            writer.writerow([name, distance, min_time, max_time, time_diff, rating, reviews])
            print(f"Processed {name}: {distance} miles, {min_time}-{max_time} mins (diff {time_diff} mins), £{delivery_cost}, {rating}, {reviews} reviews")

    print('Data has been written to deliveroo_location1.csv')

# Input desired Deliveroo URL for specific location
url = 'https://deliveroo.co.uk'
scrape_deliveroo(url)


