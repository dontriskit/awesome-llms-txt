import os
import json
import asyncio
import logging
from scraper import sanitize_domain, save_llms_file
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths
OUTPUT_DIR = "awesome-llms-txt"
METADATA_PATH = os.path.join(OUTPUT_DIR, "_metadata.json")
CONCURRENT_DOWNLOADS = 5

async def retry_missing():
    # Load metadata
    try:
        with open(METADATA_PATH, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load metadata: {e}")
        return

    # Map sanitized domain to item
    domain_map = {sanitize_domain(item.get('mainDomain', '')): item for item in metadata}
    tasks = []
    connector = aiohttp.TCPConnector(limit=CONCURRENT_DOWNLOADS)
    async with aiohttp.ClientSession(connector=connector) as session:
        for domain_dir in os.listdir(OUTPUT_DIR):
            dpath = os.path.join(OUTPUT_DIR, domain_dir)
            if not os.path.isdir(dpath):
                continue
            # Check for any .txt files
            if any(fname.endswith('.txt') for fname in os.listdir(dpath)):
                continue
            item = domain_map.get(domain_dir)
            if not item:
                logging.warning(f"No metadata for directory {domain_dir}, skipping.")
                continue
            logging.info(f"Retrying download for {domain_dir}")
            tasks.append(save_llms_file(session, item, OUTPUT_DIR))
        if tasks:
            await asyncio.gather(*tasks)
        else:
            logging.info("No missing llms.txt to retry.")

if __name__ == '__main__':
    asyncio.run(retry_missing())
