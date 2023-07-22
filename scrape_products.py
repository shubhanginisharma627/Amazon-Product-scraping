import csv
import requests
from bs4 import BeautifulSoup

def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for item in soup.select('div.s-asin'):
        product_url = "https://www.amazon.in" + item.select_one('h2 > a')['href']
        product_name = item.select_one('h2 > a > span').text.strip()

        # Handle missing product price gracefully
        product_price_elem = item.select_one('span.a-price > span.a-offscreen')
        product_price = product_price_elem.text.strip() if product_price_elem else 'Price not available'

        rating = item.select_one('span.a-icon-alt')
        product_rating = rating.text if rating else 'Not rated'
        num_reviews = item.select_one('span.a-size-base').text.strip() if rating else '0 reviews'

        products.append({
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': product_rating,
            'Number of Reviews': num_reviews,
        })

    return products

def scrape_multiple_pages(num_pages):
    base_url = "https://www.amazon.in/s"
    params = {
        'k': 'bags',
        'crid': '2M096C61O4MLT',
        'qid': '1653308124',
        'sprefix': 'ba%2Caps%2C283',
        'ref': 'sr_pg_',
    }

    all_products = []
    for page_num in range(1, num_pages + 1):
        params['page'] = page_num
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = scrape_product_page(response.url)
        all_products.extend(products)

    return all_products

if __name__ == "__main__":
    num_pages_to_scrape = 20
    all_products_data = scrape_multiple_pages(num_pages_to_scrape)

    # Export data to CSV
    csv_file = "amazon_products.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_products_data)

    print(f"Scraped {len(all_products_data)} products and saved to {csv_file}.")
