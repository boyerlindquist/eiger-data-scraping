from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pandas as pd

# Read CSV file
# file csv jaket: eiger_product.csv
# file csv kemeja: eiger_kemeja.csv
# file csv tas: eiger_tas.csv

df = pd.read_csv("eiger_tas.csv")
product_links_list = df["Product_Link"].tolist()

# Initialize WebDriver
driver = webdriver.Chrome()

# List to store extracted data
product_data = []

# Function to wait for elements and retry on stale reference
def wait_for_element(driver, by, value, timeout=10, retries=3):
    """Waits for an element to be present with retries if it becomes stale."""
    for attempt in range(retries):
        try:
            return WebDriverWait(driver, timeout, ignored_exceptions=[StaleElementReferenceException]).until(
                EC.presence_of_element_located((by, value))
            )
        except StaleElementReferenceException:
            print(f"Retrying to locate {value} (attempt {attempt+1})...")

    raise TimeoutException(f"Failed to locate {value} after {retries} attempts.")

# Scrape each product
for url in product_links_list:
    print(f"Scraping {url}...")
    driver.get(url)

    try:
        # Wait and retry for key elements
        variant_card = wait_for_element(driver, By.CLASS_NAME, "eiger-styles-Wly8hl")
        picture = WebDriverWait(driver, 10, ignored_exceptions=[StaleElementReferenceException]).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eiger-styles-_4ANpzS.eiger-styles-oAUkSW.eiger-styles-o9qbKW.m_d98df724.mantine-Carousel-slide"))
        )
        about = wait_for_element(driver, By.CLASS_NAME, "eiger-styles-FVI8gJ")
        about_attrib = about.find_elements(By.CLASS_NAME, "eiger-styles-Oh8xeC")

        # Extract product details
        name = variant_card.find_element(By.TAG_NAME, "h1").text
        warna = variant_card.find_element(By.XPATH, './/div[4]/span/span').text
        harga = variant_card.find_element(By.XPATH, './/div[2]/div/span').text
        fotos = [foto.find_element(By.TAG_NAME, "img").get_attribute("src") for foto in picture]
        sku = about_attrib[0].find_elements(By.TAG_NAME, "div")[1].text
        activity = about_attrib[1].find_elements(By.TAG_NAME, "div")[1].text
        gender = about_attrib[2].find_elements(By.TAG_NAME, "div")[1].text

        # Append data to list
        product_data.append([name, warna, harga, fotos, sku, activity, gender])

    except TimeoutException as e:
        print(f"Timeout error on {url}: {e}")
    except StaleElementReferenceException as e:
        print(f"Stale element error on {url}: {e}")
    except Exception as e:
        print(f"Error on {url}: {e}")

# Close the browser
driver.quit()

# Save to CSV
df_output = pd.DataFrame(product_data, columns=["Name", "Color", "Price", "Image URL", "SKU", "Activity", "Gender"])
df_output.to_csv("data_tas.csv", index=False)

print("Scraping completed. Data has been saved.")
