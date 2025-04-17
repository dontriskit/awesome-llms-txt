import asyncio
import json
import os
import logging
import re
from typing import List, Dict, Any, Optional

import aiohttp
import aiofiles
from playwright.async_api import async_playwright

# --- Configuration ---
TARGET_URL = "https://directory.llmstxt.cloud/"
OUTPUT_DIR = "awesome-llms-txt"
CONCURRENT_DOWNLOADS = 10  # Limit concurrent downloads
REQUEST_TIMEOUT = 20  # Seconds
USER_AGENT = "AwesomeLLMsTxtScraper/1.0 (+https://github.com/your-repo-here)" # Be a good citizen

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions ---
def sanitize_domain(domain: str) -> str:
    """Cleans a domain name to be used as a directory name."""
    sanitized = re.sub(r'^https?://', '', domain)
    sanitized = re.sub(r'^www\.', '', sanitized)
    sanitized = sanitized.rstrip('/')
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', sanitized)
    if not sanitized:
        return "unknown_domain"
    return sanitized

def process_raw_item(raw_item_data: List) -> Optional[Dict[str, Any]]:
    """Processes the specific nested JSON structure from the Astro props."""
    if not isinstance(raw_item_data, list) or len(raw_item_data) != 2:
        logging.warning(f"Unexpected raw item data format: {raw_item_data}")
        return None
    item_dict = raw_item_data[1]
    if not isinstance(item_dict, dict):
         logging.warning(f"Expected dict, got {type(item_dict)} in raw item: {raw_item_data}")
         return None

    processed = {}
    for key, value in item_dict.items():
        if isinstance(value, list) and len(value) == 2 and value[0] == 0:
            processed[key] = value[1]
        else:
            processed[key] = value

    if 'url' not in processed or 'mainDomain' not in processed:
        logging.warning(f"Skipping item due to missing 'url' or 'mainDomain': {processed}")
        return None

    if 'urlFull' in processed and not processed['urlFull']:
        processed['urlFull'] = None

    return processed

async def scrape_directory_data(url: str) -> List[Dict[str, Any]]:
    """Scrapes the llms.txt directory website using Playwright."""
    logging.info(f"Starting scrape for {url}")
    data: List[Dict[str, Any]] = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            selector = 'astro-island[component-export="DirectoryPageComponent"]'
            props_attr = await page.locator(selector).get_attribute("props")
            if not props_attr:
                logging.error("Could not find props attribute. Scraping failed.")
                return []

            raw_props = json.loads(props_attr)
            raw_items = raw_props.get("directoryItems", [])
            if len(raw_items) == 2 and raw_items[0] == 1:
                items = raw_items[1]
                logging.info(f"Found {len(items)} raw items.")
                for raw in items:
                    proc = process_raw_item(raw)
                    if proc:
                        data.append(proc)
            else:
                logging.error("Unexpected 'directoryItems' structure.")

        except Exception as e:
            logging.error(f"Error during scraping: {e}")
        finally:
            await browser.close()

    logging.info(f"Finished scraping. {len(data)} items collected.")
    return data

async def fetch_txt_content(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """Fetches content from a given URL, returns text or None."""
    if not url.startswith(('http://', 'https://')):
        logging.warning(f"Invalid URL: {url}")
        return None
    try:
        async with session.get(url, timeout=REQUEST_TIMEOUT, headers={'User-Agent': USER_AGENT}) as resp:
            resp.raise_for_status()
            text = await resp.text(encoding='utf-8', errors='replace')
            return text
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

async def save_llms_file(session: aiohttp.ClientSession, item: Dict[str, Any], base_dir: str):
    main_domain = item.get('mainDomain')
    if not main_domain or item.get('down'):
        return
    name = sanitize_domain(main_domain)
    dpath = os.path.join(base_dir, name)
    os.makedirs(dpath, exist_ok=True)

    for key, default in [('url', 'llms.txt'), ('urlFull', 'llms-full.txt')]:
        url = item.get(key)
        if not url or url == item.get('url') and key == 'urlFull':
            continue
        content = await fetch_txt_content(session, url)
        if not content:
            continue
        fname = os.path.basename(url) if '.' in os.path.basename(url) else default
        path = os.path.join(dpath, fname)
        try:
            async with aiofiles.open(path, 'w', encoding='utf-8') as f:
                await f.write(content)
        except Exception as e:
            logging.error(f"Write error {path}: {e}")

async def main():
    data = await scrape_directory_data(TARGET_URL)
    if not data:
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, '_metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    conn = aiohttp.TCPConnector(limit=CONCURRENT_DOWNLOADS)
    async with aiohttp.ClientSession(connector=conn) as s:
        await asyncio.gather(*(save_llms_file(s, itm, OUTPUT_DIR) for itm in data))

if __name__ == "__main__":
    asyncio.run(main())
