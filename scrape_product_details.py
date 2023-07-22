import csv
import requests
from bs4 import BeautifulSoup

def scrape_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Handle missing ASIN gracefully
    asin_elem = soup.select_one('div[data-asin]')
    asin = asin_elem['data-asin'] if asin_elem else 'ASIN not available'

    # Handle missing product description gracefully
    description_elem = soup.select_one('meta[name="description"]')
    description = description_elem['content'] if description_elem else 'Product description not available'

    manufacturer_elem = soup.select_one('a#bylineInfo')
    manufacturer = manufacturer_elem.text.strip() if manufacturer_elem else 'Manufacturer not available'

    return {
        'Product URL': product_url,
        'ASIN': asin,
        'Product Description': description,
        'Manufacturer': manufacturer,
    }

if __name__ == "__main__":
    # Load the previously scraped data from the CSV file
    csv_file = "amazon_products.csv"
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products_data = list(reader)

    # Scrape additional information for each product
    all_products_details = []
    for product in products_data:
        product_url = product['Product URL']
        product_details = scrape_product_details(product_url)
        all_products_details.append(product_details)

    # Export the complete product data to CSV
    complete_data_csv = "amazon_products_complete.csv"
    with open(complete_data_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Product URL', 'ASIN', 'Product Description', 'Manufacturer']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_products_details)

    print(f"Scraped additional details for {len(all_products_details)} products and saved to {complete_data_csv}.")
