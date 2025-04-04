import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome to run headlessly
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

wait = WebDriverWait(driver, 20)

def extract_price(text):
    match = re.search(r"(\d+(\.\d+)?)", text)
    return float(match.group(1)) if match else None

# Example for one product (repeat for others)
URL_TABLE = "https://www.structube.com/en_ca/diningtblarda?pid=43107#product_description"
THRESHOLD_TABLE = 279.0

try:
    driver.get(URL_TABLE)
    # Wait until the price element loads (adjust the selector as needed)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/main/main/div[1]/div[8]/div/div/section[2]/div/div[2]")))
    text = element.text.strip()
    print("Raw price text:", text)
    price = extract_price(text)
    if price is not None:
        print("Extracted price:", price)
        if price < THRESHOLD_TABLE:
            print(f"ALERT: Price is below ${THRESHOLD_TABLE}: ${price}")
        else:
            print("Price is above threshold.")
    else:
        print("Could not extract a price.")
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
