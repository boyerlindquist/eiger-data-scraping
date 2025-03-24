# Eiger Product Scraper

This project is a web scraping tool designed to extract product information from the Eiger Adventure website. The scraper collects data from three product categories: jackets, shirts, and backpacks. The project consists of two main scripts:

1. **Product Links Scraper**: Gathers product links from multiple pages.
2. **Product Details Scraper**: Uses the collected links to extract detailed product information.

## Tools & Technologies Used
- **Python**: Primary programming language
- **Requests**: Fetching HTML content
- **BeautifulSoup**: Parsing HTML for product links
- **Selenium**: Extracting dynamic content from product pages
- **Pandas**: Data processing and CSV handling
- **Chrome WebDriver**: Automating browser interaction

## Data Extraction Details

The scraper extracts the following fields:

- **Product_Name**: The name of the product
- **Product_Link**: The URL to the product page
- **Color**: Available color variant of the product
- **Price**: The displayed price of the product
- **Image URL**: List of image URLs of the product
- **SKU**: Unique product identifier
- **Activity**: Suggested activity for the product
- **Gender**: Targeted gender category

## Scraping Process
1. The first script iterates through the paginated category pages to collect product links.
2. The second script loads each product page, waits for elements to be available, and extracts the required details.
3. Extracted data is stored in CSV files (`data_jaket.csv`, `data_kemeja.csv`, and `data_tas.csv`).

