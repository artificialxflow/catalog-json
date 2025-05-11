# Sitemap Product Image Scraper

## Overview
This Streamlit app allows you to input a sitemap URL (e.g., from xml-sitemaps.com), scrapes the website for product pages, and outputs a JSON file containing product image URLs and product names.

## Setup
1. Install dependencies:
   ```sh
   pnpm install
   ```
   or, if using pip:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app:
   ```sh
   streamlit run app/streamlit_sitemap_scraper.py
   ```

## Usage
- Enter the sitemap URL in the input field (example provided).
- Click the "Scrape Sitemap" button.
- The app will display a preview and allow you to download the results as a JSON file.

## Output
- The JSON file contains a list of objects with `product_url`, `product_name`, and `image_url` fields.

## Notes
- The app uses heuristics to identify product pages and extract product info. For custom sites, you may need to adjust the scraping logic in `app/streamlit_sitemap_scraper.py`. 