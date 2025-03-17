import requests
import pandas as pd
import time
import re
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# Default business categories (if user doesn't specify)
DEFAULT_BUSINESS_TYPES = {
    "lawyer": "best lawyer in {city}",
    "surgeon": "top surgeon in {city}",
    "dentist": "best dentist near {city}",
    "financial_advisor": "financial advisor in {city}",
    "custom_home_builder": "custom home builder in {city}",
    "roofing_company": "roofing company in {city}",
    "solar_installer": "solar panel installer in {city}",
    "hvac_company": "hvac repair company in {city}",
    "kitchen_remodeler": "kitchen remodeling contractor in {city}",
    "pool_builder": "pool builder in {city}",
    "foundation_repair": "foundation repair company in {city}",
    "electrician": "best electrician in {city}"
}

ua = UserAgent()

def get_businesses(city_name, business_types=None, max_per_industry=180):
    businesses = []

    # Use user-specified business types or default to predefined list
    if business_types:
        business_dict = {b: f"best {b} in {city_name}" for b in business_types}
    else:
        business_dict = {k: v.format(city=city_name) for k, v in DEFAULT_BUSINESS_TYPES.items()}

    for industry, query in business_dict.items():
        print(f"Fetching businesses for {industry} in {city_name}...")

        next_page_token = None
        industry_count = 0

        while industry_count < max_per_industry:
            url = "https://places.googleapis.com/v1/places:searchText"
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.businessStatus,places.nationalPhoneNumber,places.websiteUri"
            }
            data = {"textQuery": query, "pageSize": 20}
            if next_page_token:
                data["pageToken"] = next_page_token

            response = requests.post(url, headers=headers, json=data).json()

            if "places" in response:
                for place in response["places"]:
                    if industry_count >= max_per_industry:
                        break

                    businesses.append({
                        "name": place.get("displayName", {}).get("text", "N/A"),
                        "address": place.get("formattedAddress", "N/A"),
                        "phone": place.get("nationalPhoneNumber", "N/A"),
                        "website": place.get("websiteUri", "N/A"),
                        "is_claimed": "Yes" if place.get("businessStatus") == "OPERATIONAL" else "No",
                        "industry": industry,
                        "city": city_name,
                    })

                    industry_count += 1

            next_page_token = response.get("nextPageToken", None)
            if not next_page_token:
                break  
            time.sleep(2)

    return businesses

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python seo_scraper.py '<city>' '<business_type1, business_type2>'")
        sys.exit(1)

    city_name = sys.argv[1]

    # Parse business types from input
    business_types = sys.argv[2].split(",") if len(sys.argv) > 2 else None

    print(f"Fetching business data for {city_name}...")

    business_data = get_businesses(city_name, business_types)
    df = pd.DataFrame(business_data)

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Save with today's date
    today = datetime.today().strftime('%Y-%m-%d')
    output_file = f"data/outreach_{today}.csv"
    df.to_csv(output_file, index=False)

    print(f"✅ Outreach list saved as {output_file}!")
