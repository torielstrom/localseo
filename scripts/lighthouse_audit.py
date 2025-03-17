import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("PAGESPEED_API_KEY")

# Function to find the latest outreach file
def get_latest_outreach_file():
    """Find the most recent outreach file based on date."""
    data_dir = "data"
    files = [f for f in os.listdir(data_dir) if f.startswith("outreach_") and f.endswith(".csv")]

    # Function to check if a filename contains a valid YYYY-MM-DD date
    def is_valid_date(filename):
        try:
            date_part = filename[9:19]  # Extract YYYY-MM-DD
            datetime.strptime(date_part, "%Y-%m-%d")  # Try parsing it
            return True
        except ValueError:
            return False  # Not a valid date format

    # Filter valid files
    files = [f for f in files if is_valid_date(f)]

    if not files:
        print("❌ No valid outreach files found.")
        return None

    # Sort by date, latest first
    latest_file = sorted(files, reverse=True)[0]
    return os.path.join(data_dir, latest_file)

# Find latest outreach file
csv_filename = get_latest_outreach_file()

if not csv_filename:
    print("❌ No valid outreach file found. Exiting.")
    exit()

df = pd.read_csv(csv_filename)

def audit_website(url):
    """Fetches Lighthouse audit results for a website using Google's PageSpeed API."""
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={API_KEY}&category=performance&category=seo&category=best-practices"
    
    try:
        response = requests.get(api_url)
        data = response.json()

        # Extract key scores
        lighthouse_scores = {
            "Performance Score": data["lighthouseResult"]["categories"]["performance"]["score"] * 100,
            "SEO Score": data["lighthouseResult"]["categories"]["seo"]["score"] * 100,
            "Best Practices Score": data["lighthouseResult"]["categories"]["best-practices"]["score"] * 100
        }

        print(f"✅ {url} - Performance: {lighthouse_scores['Performance Score']}, SEO: {lighthouse_scores['SEO Score']}, Best Practices: {lighthouse_scores['Best Practices Score']}")
        return lighthouse_scores

    except Exception as e:
        print(f"❌ Error auditing {url}: {str(e)}")
        return {"Performance Score": "Error", "SEO Score": "Error", "Best Practices Score": "Error"}

# Run audits for each website and append results
for index, row in df.iterrows():
    website = str(row.get("website", "")).strip()  
    
    if website and website.lower() != "n/a":
        print(f"🔍 Auditing: {website}...")
        scores = audit_website(website)
        
        # Update dataframe with new scores
        df.at[index, "Performance Score"] = scores["Performance Score"]
        df.at[index, "SEO Score"] = scores["SEO Score"]
        df.at[index, "Best Practices Score"] = scores["Best Practices Score"]

        time.sleep(3)  

# Save results back to the latest CSV file
df.to_csv(csv_filename, index=False)
print(f"📂 Lighthouse audit results appended to {csv_filename}!")
