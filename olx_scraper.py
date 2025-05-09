import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.olx.in/items/q-car-cover"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_olx_car_covers(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    items = []

    for listing in soup.find_all("li", class_="EIR5N"):
        title_tag = listing.find("span", class_="_2tW1I")
        price_tag = listing.find("span", class_="_89yzn")
        location_tag = listing.find("span", class_="_2FYw6")

        if title_tag and price_tag and location_tag:
            items.append({
                "title": title_tag.text.strip(),
                "price": price_tag.text.strip(),
                "location": location_tag.text.strip()
            })

    return items

def save_to_csv(data, filename="olx_car_covers.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "location"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    print("Scraping OLX car covers...")
    results = scrape_olx_car_covers(BASE_URL)
    save_to_csv(results)
    print(f"Saved {len(results)} items to 'olx_car_covers.csv'")
