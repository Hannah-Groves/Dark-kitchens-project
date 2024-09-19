### SCRAPING DATA FROM JUST EAT WEBSITE ###

# Install and import necessary packages
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# This code uses Google Chrome as the search engine for the Just Eat webpage
# Path to ChromeDriver (insert here the path to the chromedriver.exe file on your device)
webdriver_path = r'C:\Users\chromedriver.exe'

# Set up Chrome options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Prepare Google Chrome for search
service = Service(executable_path=webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

# This function compiles a list of all the food delivery establishments listed on the Just Eat website provided
def get_restaurant_links(url):
    driver.get(url)
    
    # Check webpage has properly loaded before retrieving links
    input("Check the browser that it has loaded the page and press Enter here...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page.")
            break
        last_height = new_height

    # Make list of all the links
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/menu"]')
    restaurant_links = [link.get_attribute('href') for link in links]
    
    # Print statement with the number of links collected
    print(f"Found {len(restaurant_links)} restaurant links.")
    return restaurant_links


# Loop through the links for all establishments
def get_restaurant_data(restaurant_url):
    driver.get(restaurant_url)
    
    # Page loading time
    time.sleep(3)

    # Find establishment name
    try:
        name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="restaurant-heading"]'))).text.strip()
    except Exception as e:
        name = "No Name Found"
        print(f"Error getting name: {str(e)}")

    # Find establishment address
    try:
        address = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="header-restaurantAddress"]'))).text.strip()
    except Exception as e:
        address = "No Address Found"
        print(f"Error getting address: {str(e)}")

    # Find cuisine type
    try:
        cuisines = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-js-test="header-cuisines"]'))).text.strip().replace('\n', ', ')
    except Exception as e:
        cuisines = "No Cuisines Found"
        print(f"Error getting cuisines: {str(e)}")

    # Find star rating
    try:
        star_rating = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="rating-description"]'))).text.split()[0]
    except Exception as e:
        star_rating = "No Rating Found"
        print(f"Error getting star rating: {str(e)}")

    # Find number of reviews
    try:
        number_of_reviews = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="rating-count-description"]'))).text.split()[1]
    except Exception as e:
        number_of_reviews = "No Reviews Found"
        print(f"Error getting number of reviews: {str(e)}")

    # Find delivery times
    try:
        delivery_times = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.c-basketSwitcher-eta'))).text.strip()
    except Exception as e:
        delivery_times = "Delivery Time Info Not Available"
        print(f"Error getting delivery times: {str(e)}")

    # Find delivery fees
    try:
        delivery_fee = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.c-orderStatus-deliveryFee'))).text.strip()
    except Exception as e:
        delivery_fee = "Delivery Fee Info Not Available"
        print(f"Error getting delivery fee: {str(e)}")

    # Find collection availability
    try:
        collection_available = 'Yes' if "collect" in WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="restaurant-header-service-type-switcher"]'))).text.lower() else 'No'
    except Exception as e:
        collection_available = "No Collection"
        print(f"Error checking collection availability: {str(e)}")

    # Collect all data into a list of lists
    data = [name, address, cuisines, star_rating, number_of_reviews, delivery_times, delivery_fee, collection_available]
    return data


# Input desired Just Eat URL for specific location
def main():
    url = "https://www.just-eat.co.uk"
    restaurant_links = get_restaurant_links(url)
    
    # Create a CSV file and copy all extracted data to it
    with open('justeat_location1.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Restaurant Name', 'Address', 'Cuisines', 'Star Rating', 'Number of Reviews', 'Delivery Times', 'Delivery Fee', 'Collection Available'])
        
        for link in restaurant_links:
            data = get_restaurant_data(link)
            writer.writerow(data)
            
    print("Data collection complete and written to CSV.")
    driver.quit()

if __name__ == "__main__":
    main()

