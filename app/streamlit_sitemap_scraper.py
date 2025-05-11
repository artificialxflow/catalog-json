import streamlit as st
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
from io import BytesIO, StringIO
from urllib.parse import urlparse, urljoin

# --- Streamlit UI ---
st.title('Sitemap Product Image Scraper')
st.write('Enter a sitemap URL (e.g., from xml-sitemaps.com) to extract product image URLs and names.')

sitemap_url = st.text_input('Sitemap URL', value='https://www.xml-sitemaps.com/download/ronakelectronic.ir-2d83255a7/sitemap.xml?view=1')

# Helper to fetch and parse sitemap
def fetch_sitemap_urls(sitemap_url):
    resp = requests.get(sitemap_url)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [elem.text for elem in root.findall('.//ns:loc', ns)]
    return urls

# Helper to extract product name and image from a page
def extract_product_info(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Try to find a product container
        container = None
        for selector in [
            '.product', '.product-detail', '.product-details', '.woocommerce-product-details',
            '.single-product', '.product-info', '.product-content', '.product-page', '.product-view',
        ]:
            container = soup.select_one(selector)
            if container:
                break
        name, img_url = None, None
        if container:
            # Name: h1 or h2 inside container
            name_tag = container.find(['h1', 'h2'])
            name = name_tag.get_text(strip=True) if name_tag else None
            # Image: try common selectors inside container
            for img_selector in [
                'img.wp-post-image', 'img.attachment-shop_single', 'img.attachment-woocommerce_thumbnail',
                'img',
            ]:
                img = container.select_one(img_selector)
                if img and img.has_attr('src'):
                    img_url = img['src']
                    break
        # Fallback to global search if not found in container
        if not name:
            name_tag = soup.find(['h1', 'h2'])
            name = name_tag.get_text(strip=True) if name_tag else None
        if not img_url:
            for selector in [
                '.product img', '.woocommerce-product-gallery__image img', '.gallery img', '.product-image img',
                'img.wp-post-image', 'img.attachment-shop_single', 'img.attachment-woocommerce_thumbnail', 'img'
            ]:
                img = soup.select_one(selector)
                if img and img.has_attr('src'):
                    img_url = img['src']
                    break
        if img_url and img_url.startswith('/'):
            img_url = urljoin(url, img_url)
        return name, img_url
    except Exception:
        return None, None

# Helper to extract domain name for file naming
def get_domain_from_sitemap_url(sitemap_url):
    import re
    parsed = urlparse(sitemap_url)
    match = re.search(r'([a-zA-Z0-9\-]+\.[a-zA-Z]{2,})', sitemap_url)
    if match:
        return match.group(1)
    return parsed.netloc or 'products'

# --- Scraper Section ---
st.header('Step 1: Scrape a Sitemap')
if st.button('Scrape Sitemap'):
    if not sitemap_url:
        st.error('Please enter a sitemap URL.')
    else:
        with st.spinner('Fetching sitemap and scraping product pages...'):
            try:
                urls = fetch_sitemap_urls(sitemap_url)
                product_urls = [u for u in urls if '/product/' in u]
                results = []
                for u in product_urls:
                    name, img_url = extract_product_info(u)
                    if name and img_url:
                        results.append({'product_name': name, 'image_url': img_url})
                st.success(f'Found {len(results)} products.')
                st.json(results[:5])  # Show a preview
                domain = get_domain_from_sitemap_url(sitemap_url)
                file_name = f'{domain}.json'
                json_bytes = BytesIO(json.dumps(results, ensure_ascii=False, indent=2).encode('utf-8'))
                st.download_button('Download JSON', data=json_bytes, file_name=file_name, mime='application/json')
            except Exception as e:
                st.error(f'Error: {e}')

# --- Catalog Viewer Section ---
st.header('Step 2: Upload and View Product Catalog')
uploaded_file = st.file_uploader('Upload a product JSON file', type=['json'])

def render_catalog_html(products, catalog_title="Product Catalog"):
    # Responsive CSS grid and card styles
    html = f'''
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body {{ background: #f8f9fa; margin: 0; font-family: 'Segoe UI', Arial, sans-serif; }}
    .catalog-header {{
        background: linear-gradient(90deg, #007bff 0%, #00c6ff 100%);
        color: white;
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        font-size: 2.2rem;
        font-weight: bold;
        letter-spacing: 2px;
        border-radius: 0 0 1.5rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        line-height: 1.3;
    }}
    .catalog-header .contact {{
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.7rem;
        color: #e0f7fa;
    }}
    .catalog-footer {{
        background: #222;
        color: #fff;
        text-align: center;
        padding: 1.5rem 1rem 2rem 1rem;
        font-size: 1.2rem;
        border-radius: 1.5rem 1.5rem 0 0;
        margin-top: 2rem;
        letter-spacing: 1px;
    }}
    .catalog-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        padding: 2rem 2vw;
        max-width: 1200px;
        margin: 0 auto;
    }}
    .product-card {{
        background: #fff;
        border-radius: 1rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.10);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: transform 0.15s, box-shadow 0.15s;
        padding-bottom: 1.5rem;
    }}
    .product-card:hover {{
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 8px 32px rgba(0,0,0,0.16);
    }}
    .product-img {{
        width: 100%;
        max-width: 240px;
        aspect-ratio: 4/3;
        object-fit: contain;
        background: #f0f0f0;
        margin-bottom: 1rem;
        border-bottom: 1px solid #eee;
    }}
    .product-name {{
        font-size: 1.1rem;
        font-weight: 600;
        color: #222;
        text-align: center;
        margin: 0 1rem;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
    }}
    @media (max-width: 900px) {{
        .catalog-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 600px) {{
        .catalog-header {{ font-size: 1.2rem; padding: 1.2rem 0.5rem 0.5rem 0.5rem; }}
        .catalog-footer {{ font-size: 1rem; padding: 1rem 0.5rem 1.2rem 0.5rem; }}
        .catalog-grid {{ padding: 1rem 0.5vw; gap: 1rem; grid-template-columns: 1fr; }}
        .product-card {{ border-radius: 0.7rem; }}
    }}
    </style>
    </head>
    <body>
        <div class="catalog-header">
            MadeByPersians.ir<br>
            <span class="contact">email: info@madebypersians.ir &nbsp; | &nbsp; WhatsApp: +989214843361</span>
        </div>
        <div class="catalog-grid">
    '''
    for product in products:
        html += f'''
        <div class="product-card">
            <img class="product-img" src="{product['image_url']}" alt="{product['product_name']}">
            <div class="product-name">{product['product_name']}</div>
        </div>
        '''
    html += '''</div>
        <div class="catalog-footer">End of Catalog &copy; 2024</div>
    </body>
    </html>'''
    return html

if uploaded_file is not None:
    try:
        products = json.load(uploaded_file)
        # --- Deletable product cards in Streamlit ---
        st.markdown('<div style="text-align:center; font-size:2em; font-weight:bold; margin-bottom:1em;">Product Catalog</div>', unsafe_allow_html=True)
        # Use session state to persist deletions
        if 'catalog_products' not in st.session_state or st.session_state['catalog_products_file'] != uploaded_file.name:
            st.session_state['catalog_products'] = products
            st.session_state['catalog_products_file'] = uploaded_file.name
        catalog_products = st.session_state['catalog_products']
        # Show cards in rows of 3 on desktop
        to_delete = []
        for i in range(0, len(catalog_products), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx < len(catalog_products):
                    product = catalog_products[idx]
                    with cols[j]:
                        st.image(product['image_url'], use_container_width=True)
                        st.markdown(f'<div style="text-align:center; font-weight:500; margin-bottom:0.5em;">{product["product_name"]}</div>', unsafe_allow_html=True)
                        if st.button(f"Delete", key=f"delete_{idx}"):
                            to_delete.append(idx)
        # Actually delete after rendering to avoid index issues
        if to_delete:
            for idx in sorted(to_delete, reverse=True):
                del catalog_products[idx]
            st.session_state['catalog_products'] = catalog_products
            st.experimental_rerun()
        # Download as HTML
        catalog_html = render_catalog_html(catalog_products)
        st.download_button('Download Catalog as HTML', data=catalog_html, file_name='catalog.html', mime='text/html')
        # Download as JSON (optional)
        st.download_button('Download This Catalog JSON', data=json.dumps(catalog_products, ensure_ascii=False, indent=2), file_name=uploaded_file.name, mime='application/json')
    except Exception as e:
        st.error(f'Could not read or display the JSON file: {e}')

# --- Documentation ---
st.markdown('''---\n**Approach:**\n- Step 1: Scrape a sitemap and download a product JSON.\n- Step 2: Upload a product JSON to view as a responsive catalog.\n- Each product is shown in a beautiful card.\n- The catalog has a styled header and footer with contact info.\n- Products can be deleted before download.\n- Download the catalog as HTML or JSON.\n''') 