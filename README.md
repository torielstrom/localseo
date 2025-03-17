# 📍 Local SEO & Website Speed Analyzer

## 🚀 Overview
This tool fetches **local business data** from Google Places API, then runs **Google Lighthouse audits** to assess website performance and SEO health.

✅ **Who is this for?**
- SEO agencies & freelancers
- Digital marketers
- Local business consultants

---

## 🛠 Features
- Fetches **up to 180** local businesses per industry
- Uses **Google Places API** for business data
- Runs **Google Lighthouse audits** on business websites
- Saves results to a CSV file

---

## 📌 Requirements
- Python 3.x
- Google API keys for:
  - **Google Places API**
  - **Google PageSpeed Insights API**
- (Optional) Chrome for Lighthouse CLI audits

---

## 📦 Installation

### 1️⃣ Clone the repository:
```bash
git clone https://github.com/torielstrom/localseo.git
cd localseo
```

### 2️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

### 3️⃣ Set up your API keys:
Create a `.env` file in the root directory:
```env
GOOGLE_PLACES_API_KEY=your-google-places-api-key
PAGESPEED_API_KEY=your-pagespeed-api-key
```

---

## 🏁 Usage

### 1️⃣ Run the SEO scraper:
```bash
python scripts/seo_scraper.py "New York, NY" "lawyer, dentist, hvac_company"
```
- This fetches business data from **Google Places API** and saves it in `data/outreach_list.csv`.
- **Specify business types as a comma-separated list** (e.g., `"lawyer, dentist, hvac_company"`).
- If no business types are provided, it defaults to common industries.

### 2️⃣ Run the Lighthouse audit:
```bash
python scripts/lighthouse_audit.py
```
This enriches the CSV file with **website speed & SEO scores**.

---

## 📝 Example Output
| Business Name  | Industry      | Website       | Performance Score | SEO Score | Best Practices Score |
|---------------|--------------|--------------|-----------------|----------|--------------------|
| ABC Law Firm  | Lawyer       | abclaw.com   | 85              | 90       | 95                 |
| Solar Pros    | Solar        | solarpros.com | 78              | 80       | 88                 |

---

## 🔧 License
MIT License - Feel free to modify and improve!

---
