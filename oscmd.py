import aiohttp
import asyncio
import os
import json
import logging
import shutil
import zipfile
from tqdm.asyncio import tqdm
from aiohttp import ClientTimeout

# --- CONFIG ---
JSON_FILE = "goes here bitch"  # path to your local JSON
TEMP_DIR = "./downloads"       # temp folder for zips & extraction
CONCURRENCY = 6

# --- LOGGER SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("zip_grabber")

# ============================================================
# ============== FILE / FOLDER HELPERS =======================
# ============================================================

def merge_move(src, dst):
    """Move src into dst, overwriting if needed."""
    if os.path.isdir(src):
        if not os.path.exists(dst):
            shutil.move(src, dst)
        else:
            for item in os.listdir(src):
                merge_move(os.path.join(src, item), os.path.join(dst, item))
            os.rmdir(src)
    else:
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(src, dst)

def fix_structure(base_dir):
    """Flatten nested 'apps' and duplicate-named folders recursively."""
    changed = True
    while changed:
        changed = False
        for root, dirs, files in os.walk(base_dir, topdown=False):
            parent_name = os.path.basename(root)

            # 1. Handle nested "apps" folders
            if "apps" in dirs:
                nested_apps_path = os.path.join(root, "apps")
                logger.info(f"Found nested apps folder: {nested_apps_path}")
                for item in os.listdir(nested_apps_path):
                    merge_move(os.path.join(nested_apps_path, item),
                               os.path.join(root, item))
                os.rmdir(nested_apps_path)
                changed = True

            # 2. Handle duplicate-named subfolders (X\X → flatten)
            for d in dirs:
                if d.lower() == parent_name.lower():
                    nested_path = os.path.join(root, d)
                    logger.info(f"Unwrapping duplicate folder: {nested_path}")
                    for item in os.listdir(nested_path):
                        merge_move(os.path.join(nested_path, item),
                                   os.path.join(root, item))
                    os.rmdir(nested_path)
                    changed = True

# ============================================================
# ============== DOWNLOAD / EXTRACT HELPERS =================
# ============================================================

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

async def download_zips(json_file, out_dir, concurrency):
    with open(json_file, "r", encoding="utf-8") as f:
        apps = json.load(f)

    tasks = []
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession(timeout=ClientTimeout(total=60)) as session:
        for app in apps:
            zip_url = app.get("url", {}).get("zip")
            if zip_url:
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

def extract_and_cleanup_zips(zip_dir, extract_dir):
    """Extract all zips into extract_dir, then delete them."""
    os.makedirs(extract_dir, exist_ok=True)
    for file in os.listdir(zip_dir):
        if file.lower().endswith(".zip"):
            zip_path = os.path.join(zip_dir, file)
            logger.info(f"Extracting {zip_path}")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            os.remove(zip_path)
            logger.info(f"Deleted {zip_path} after extraction")

def move_to_target(extracted_dir, target_dir):
    """Move extracted folders into target_dir (overwrite duplicates)."""
    os.makedirs(target_dir, exist_ok=True)
    for item in os.listdir(extracted_dir):
        src = os.path.join(extracted_dir, item)
        dst = os.path.join(target_dir, item)
        merge_move(src, dst)
C:\\Users\\theam\\Downloads\\testfolder
# ============================================================
# ============== MAIN WORKFLOW ===============================
# ============================================================

async def main():
    # Ask user for target path
    target_path = input(
        "Enter the full path where you want the folders to go WITH DOUBLE BACKSLASHES or RAW STRING NOTATION (e.g. E:\\apps or r'E:\apps'): "
    ).strip()

    # NOTE: In Python, you MUST use either double backslashes (E:\\apps)
    # or raw string notation r'E:\apps'. A single backslash will NOT work.

    # 1. Download zips
    await download_zips(JSON_FILE, TEMP_DIR, CONCURRENCY)

    # 2. Extract zips and delete them
    extract_and_cleanup_zips(TEMP_DIR, TEMP_DIR)

    # 3. Move extracted folders to target
    move_to_target(TEMP_DIR, target_path)

    # 4. Fix duplicates and nested folders in target
    fix_structure(target_path)

    logger.info("✅ All tasks complete!")

if __name__ == "__main__":
    asyncio.run(main())
