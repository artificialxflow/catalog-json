# Decisions for Sitemap Product Image Scraper

## Technology Choices
- **Streamlit**: Chosen for rapid UI development and ease of use for data apps.
- **requests**: For HTTP requests to fetch sitemap and product pages.
- **BeautifulSoup**: For HTML parsing and extraction of product names and images.
- **xml.etree.ElementTree**: For parsing XML sitemaps.

## Scraping Approach
- The app fetches all URLs from the provided sitemap.
- It filters for product pages using a heuristic (`/product/` in the URL).
- For each product page, it extracts the product name (from `<h1>`) and the main image (from the first `<img>` tag).
- Results are provided as a downloadable JSON file.

## Security & Best Practices
- No sensitive data is stored or transmitted.
- All user input is validated.
- Error handling is implemented for network and parsing errors.

## Styling
- Streamlit's default styling is used for simplicity and maintainability.

## Testing
- Manual testing recommended for different sitemap structures and product page layouts.

## Future Improvements
- Make product extraction logic more robust for different site structures.
- Add automated tests for the scraping functions. 