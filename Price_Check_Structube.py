import requests
from bs4 import BeautifulSoup
import re

# Define product URLs
URL_TABLE = "https://www.structube.com/en_ca/diningtblarda?pid=43107#product_description"
URL_CHAIR = "https://www.structube.com/en_ca/komal-dining-chair-31-87-53?pid=23571#product_description"
URL_OTTOMAN = "https://www.structube.com/en_ca/kinsey-tufted-ottoman-39-46-83?pid=36106#product_description"
URL_SECTIONAL = "https://www.structube.com/en_ca/sectionalskinsey?pid=36055#product_description"

# Define price thresholds for alerts
THRESHOLD_TABLE = 279.0
THRESHOLD_CHAIR = 69.0
THRESHOLD_OTTOMAN = 149.0
THRESHOLD_SECTIONAL = 999.0

def extract_price(text):
    """
    Extract the first numeric value (integer or decimal) from a text string.
    """
    match = re.search(r"(\d+(\.\d+)?)", text)
    if match:
        return float(match.group(1))
    return None

def check_price(url, css_selector, threshold, item_name):
    """
    Fetches the page at 'url', extracts the price from the element
    matching 'css_selector', compares it to 'threshold', and prints alerts.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching {item_name} page. Status code: {response.status_code}")
            return
        
        # Parse the HTML using BeautifulSoup's built-in parser
        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.select_one(css_selector)
        if not element:
            print(f"Could not find the price element for {item_name}")
            return
        
        price_text = element.get_text().strip()
        print(f"Raw {item_name} price text: {price_text}")
        
        price = extract_price(price_text)
        if price is not None:
            print(f"{item_name} Price: ${price}")
            if price < threshold:
                print(f"ALERT: {item_name} price is below ${threshold}: ${price}")
            else:
                print(f"{item_name} price is above the threshold.")
        else:
            print(f"Could not extract price for {item_name}")
    except Exception as e:
        print(f"An error occurred while checking {item_name}: {e}")

# CSS selectors derived from provided XPaths or approximated by similar structure.
# (These selectors are fragile; if Structube updates their HTML, you'll need to adjust them.)
css_table = ("body > div:nth-of-type(5) > div:nth-of-type(1) > main > main > "
             "div:nth-of-type(1) > div:nth-of-type(8) > div > div > section:nth-of-type(2) > div > div:nth-of-type(2)")
css_chair = ("body > div:nth-of-type(5) > div:nth-of-type(1) > main > main > "
             "div:nth-of-type(1) > div:nth-of-type(5) > div > div > section:nth-of-type(2) > div > div:nth-of-type(2)")
# These two selectors are assumed based on similar structure. You may need to inspect the pages.
css_ottoman = ("body > div:nth-of-type(5) > div:nth-of-type(1) > main > main > "
               "div:nth-of-type(1) > div:nth-of-type(7) > div > div > section:nth-of-type(2) > div > div:nth-of-type(2)")
css_sectional = ("body > div:nth-of-type(5) > div:nth-of-type(1) > main > main > "
                 "div:nth-of-type(1) > div:nth-of-type(6) > div > div > section:nth-of-type(2) > div > div:nth-of-type(2)")

print("Checking Dining Table Price:")
check_price(URL_TABLE, css_table, THRESHOLD_TABLE, "Dining Table")

print("\nChecking Dining Chair Price:")
check_price(URL_CHAIR, css_chair, THRESHOLD_CHAIR, "Dining Chair")

print("\nChecking Kinsey Tufted Ottoman Price:")
check_price(URL_OTTOMAN, css_ottoman, THRESHOLD_OTTOMAN, "Kinsey Tufted Ottoman")

print("\nChecking Sectional Kinsey Price:")
check_price(URL_SECTIONAL, css_sectional, THRESHOLD_SECTIONAL, "Sectional Kinsey")
