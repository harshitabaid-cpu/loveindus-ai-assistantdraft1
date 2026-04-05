# scrape_products.py
import requests
from bs4 import BeautifulSoup
import time

def scrape_products():
    """
    Upgraded Scraper: 
    1. Grabs product links from the main catalog.
    2. Visits each product page to extract deep educational data for the AI.
    """
    
    # Target brand (Example: The Ordinary or Paula's Choice)
    catalog_url = "https://theordinary.com/en-us/category/skincare" 
    base_url = "https://theordinary.com"
    
    # ⚠️ CRITICAL: Disguise the Python script as a real web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        print(f"🕵️‍♂️ Scanning catalog: {catalog_url}")
        r = requests.get(catalog_url, headers=headers, timeout=10)
        
        # If the website blocks us, we catch it immediately
        if r.status_code != 200:
            print(f"⚠️ Website blocked the scraper (Status Code: {r.status_code}).")
            return get_fallback_data()

        soup = BeautifulSoup(r.text, "html.parser")
        products = []
        
        # Step 1: Find all individual product links (Adjust selector based on actual site)
        product_cards = soup.select("a.product-link") # Example class
        product_links = [base_url + card['href'] for card in product_cards if 'href' in card.attrs][:5] # Limit to 5 for testing
        
        print(f"🔗 Found {len(product_links)} products. Digging deeper...")

        # Step 2: Visit each product page for deep data
        for link in product_links:
            time.sleep(2) # Pause for 2 seconds so we don't get banned for clicking too fast!
            
            p_req = requests.get(link, headers=headers, timeout=10)
            p_soup = BeautifulSoup(p_req.text, "html.parser")
            
            # Extracting the rich data (These selectors will need tweaking based on the live site)
            name = p_soup.select_one("h1.product-name")
            price = p_soup.select_one("span.price")
            desc = p_soup.select_one("div.product-description")
            ingredients = p_soup.select_one("div.ingredients-list")
            how_to_use = p_soup.select_one("div.how-to-use")
            conflicts = p_soup.select_one("div.contraindications")
            
            if name and price:
                product_data = {
                    "name": name.get_text(strip=True),
                    "price": price.get_text(strip=True),
                    "description": desc.get_text(strip=True) if desc else "N/A",
                    "key_ingredients": ingredients.get_text(strip=True) if ingredients else "N/A",
                    "how_to_use": how_to_use.get_text(strip=True) if how_to_use else "N/A",
                    "conflicts": conflicts.get_text(strip=True) if conflicts else "None listed",
                    "url": link
                }
                products.append(product_data)
                print(f"✅ Successfully scraped deep data for: {product_data['name']}")

        return products if products else get_fallback_data()

    except Exception as e:
        print(f"⚠️ Scraping error: {e}")
        return get_fallback_data()

# -------------------------
# 🛡️ THE SAFETY NET
# -------------------------
def get_fallback_data():
    """If the scraper gets blocked by Cloudflare, use this rich dummy data so the AI doesn't break."""
    print("🛡️ Loading rich fallback data instead...")
    return [
        {
            "name": "Niacinamide 10% + Zinc 1%",
            "price": "$6.00",
            "description": "A high-strength vitamin and blemish formula that regulates sebum and minimizes pores.",
            "key_ingredients": "Niacinamide (Vitamin B3), Zinc PCA",
            "how_to_use": "Apply to entire face morning and evening before heavier creams.",
            "conflicts": "Do NOT use with pure Vitamin C (L-Ascorbic Acid) or Ethylated Ascorbic Acid.",
            "skin_type": ["Oily", "Blemish-prone"]
        },
        {
            "name": "AHA 30% + BHA 2% Peeling Solution",
            "price": "$9.50",
            "description": "A 10-minute exfoliating facial for deep pore clearing and radiant skin.",
            "key_ingredients": "Glycolic Acid, Lactic Acid, Salicylic Acid",
            "how_to_use": "Use ideally in the PM, no more frequently than twice per week. Leave on for no more than 10 minutes.",
            "conflicts": "Do NOT use with direct acids, direct Vitamin C, Retinoids, or Peptides.",
            "skin_type": ["Normal", "Oily", "Combination"]
        }
    ]

if __name__ == "__main__":
    data = scrape_products()
    print("\n--- FINAL DATA ---")
    for p in data:
        print(f"\n{p['name']} ({p['price']})")
        print(f"Conflicts: {p.get('conflicts', 'N/A')}")
