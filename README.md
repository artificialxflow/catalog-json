# Sitemap Product Image Scraper

A simple, maintainable Streamlit app to extract product image URLs and product names from any website sitemap (e.g., from xml-sitemaps.com). The app scrapes all product pages listed in the sitemap and outputs a downloadable JSON file.

## Features
- Input any sitemap URL (XML format)
- Automatically finds product pages (heuristic: `/product/` in URL)
- Extracts product name (`<h1>`) and main image (`<img>`) from each product page
- Download results as a JSON file
- User-friendly Streamlit interface
- Error handling and progress feedback

## Quick Start
1. **Install dependencies**
   ```sh
   pnpm install
   # or
   pip install -r requirements.txt
   ```
2. **Run the app**
   ```sh
   streamlit run app/streamlit_sitemap_scraper.py
   ```
3. **Use the app**
   - Enter a sitemap URL (example provided in the app)
   - Click "Scrape Sitemap"
   - Download the JSON file with product info

## Output Format
Each entry in the JSON file contains:
```json
{
  "product_url": "...",
  "product_name": "...",
  "image_url": "..."
}
```

## Project Structure
```
project/
├── app/
│   └── streamlit_sitemap_scraper.py
├── docs/
│   ├── DECISIONS.md
│   └── README.md
├── requirements.txt
├── .gitignore
└── README.md (this file)
```

## Documentation
- [docs/README.md](docs/README.md): Detailed usage and setup
- [docs/DECISIONS.md](docs/DECISIONS.md): Technology and design decisions

## Customization
- The scraping logic is simple and may need adjustment for different website structures. See comments in `app/streamlit_sitemap_scraper.py`.

## Security & Best Practices
- No sensitive data is stored or transmitted
- All user input is validated
- Error handling is implemented

## License
MIT (add your license here if different) 