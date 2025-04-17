import os
import json
import asyncio
import logging
import os
import aiohttp
from scraper import sanitize_domain, save_llms_file

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths
OUTPUT_DIR = "websites"
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
            item = domain_map.get(domain_dir)
            if not item:
                logging.warning(f"No metadata for directory {domain_dir}, skipping.")
                continue
            if item.get('skipCheck', False):
                logging.info(f"Skipping {domain_dir} due to skipCheck flag")
                continue
            files = os.listdir(dpath)
            missing_llms = 'llms.txt' not in files
            missing_full = bool(item.get('urlFull')) and 'llms-full.txt' not in files
            if not missing_llms and not missing_full:
                continue
            logging.info(f"Retrying download for {domain_dir}, missing_llms={missing_llms}, missing_full={missing_full}")
            tasks.append(save_llms_file(session, item, OUTPUT_DIR))
        if tasks:
            await asyncio.gather(*tasks)
        else:
            logging.info("No missing llms.txt to retry.")

    # Cleanup empty directories after retry
    for domain_dir in os.listdir(OUTPUT_DIR):
        dir_path = os.path.join(OUTPUT_DIR, domain_dir)
        if os.path.isdir(dir_path) and not os.listdir(dir_path):
            logging.info(f"Removing empty directory {domain_dir}")
            try:
                os.rmdir(dir_path)
            except Exception as e:
                logging.error(f"Failed to remove directory {domain_dir}: {e}")

if __name__ == '__main__':
    asyncio.run(retry_missing())
