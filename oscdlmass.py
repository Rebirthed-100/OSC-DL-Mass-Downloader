import aiohttp
import asyncio
import os
import json
import logging
from tqdm.asyncio import tqdm
from aiohttp import ClientTimeout

# --- CONFIG ---
JSON_FILE = "goes here bitch"  # path to your local JSON
OUT_DIR = "./apps"
CONCURRENCY = 6

# --- LOGGER SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("zip_grabber")

# --- DOWNLOAD FILE ---
async def download_file(session, url, outpath):
    try:
        async with session.get(url) as r:
            if r.status != 200:
                logger.warning(f"Failed {url}: HTTP {r.status}")
                return False
            content = await r.read()
            os.makedirs(os.path.dirname(outpath), exist_ok=True)
            with open(outpath, "wb") as f:
                f.write(content)
            logger.info(f"Saved {outpath} ({len(content)} bytes)")
            return True
    except Exception as e:
        logger.exception(f"Error downloading {url}: {e}")
        return False

# --- DOWNLOAD ALL ZIPS FROM JSON ---
async def download_zips(json_file, out_dir, concurrency):
    with open(json_file, "r", encoding="utf-8") as f:
        apps = json.load(f)

    # Collect all zip URLs
    tasks = []
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession(timeout=ClientTimeout(total=60)) as session:
        for app in apps:
            zip_url = app.get("url", {}).get("zip")  # <-- look inside "url"
            if zip_url:
                # Save all zips directly inside OUT_DIR
                filename = os.path.join(out_dir, os.path.basename(zip_url))
                
                async def sem_task(url=zip_url, path=filename):
                    async with sem:
                        await download_file(session, url, path)

                tasks.append(sem_task())

        if not tasks:
            logger.warning("No .zip URLs found in JSON.")
            return

        pbar = tqdm(total=len(tasks), desc="Downloading zips", unit="file")
        for coro in asyncio.as_completed(tasks):
            await coro
            pbar.update(1)
        pbar.close()
        logger.info("All downloads complete.")

# --- ENTRY POINT ---
if __name__ == "__main__":
    asyncio.run(download_zips(JSON_FILE, OUT_DIR, CONCURRENCY))
