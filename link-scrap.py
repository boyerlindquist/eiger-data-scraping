import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Headers to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

data = []

# url jaket: https://www.eigeradventure.com/en/apparel/jacket?page={page}&order=price-desc
# url kemeja: https://www.eigeradventure.com/en/apparel/shirt?page={page}&order=price-asc
# url tas punggung: https://www.eigeradventure.com/en/bags/backpack?page={page}&order=price-asc

# Loop through pages
for page in range(1, 10):  
    url = f"https://www.eigeradventure.com/en/bags/backpack?page={page}&order=price-asc"
    
    print(f"Scraping page {page}...")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}, skipping...")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = soup.find_all("div", class_="eiger-styles-MRPLkg eiger-styles-vrZjuc")  

    # Loop through products and extract details
    for product in products:
        try:
            product_name = product.find("a", class_="eiger-styles-ISzWsP").text.strip()
            product_link_tag = product.find("a", class_="eiger-styles-wX_6Tz")  # Find <a> tag with class
            product_link = product_link_tag.get("href") if product_link_tag else "No Link"

            # If the link is relative, prepend the base URL
            if product_link.startswith("/"):
                product_link = f"https://www.eigeradventure.com{product_link}"

            data.append({
                "Product_Name": product_name,
                "Product_Link": product_link
            })

        except AttributeError:
            continue  # Skip if any attribute is missing

    time.sleep(2)  # Delay to avoid being blocked

# Convert to Pandas DataFrame
df = pd.DataFrame(data)
df.to_csv("eiger_tas.csv", index=False)

print("Scraping complete! Data saved to eiger_products.csv")
