# scrape_products.py
import requests
from bs4 import BeautifulSoup

def scrape_products():
    url = "https://loveindus.com/collections/all-products"  # main product catalog
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    products = []

    # Loop through product cards
    for card in soup.select("div.product-card"):  # adjust selector if needed
        name_tag = card.select_one("h2.product-card__title")
        price_tag = card.select_one("span.price")
        desc_tag = card.select_one("p.product-card__description")
        
        if name_tag and price_tag:
            product = {
                "name": name_tag.get_text(strip=True),
                "price": price_tag.get_text(strip=True),
                "description": desc_tag.get_text(strip=True) if desc_tag else "",
                "benefits": [],  # can be added manually later
                "skin_type": []  # optional
            }
            products.append(product)
    return products

if __name__ == "__main__":
    data = scrape_products()
    for p in data:
        print(p)
        
