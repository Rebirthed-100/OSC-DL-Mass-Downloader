# The OSCMD (Open Shop Channel Mass Downloader)
### previously the OSC-Mass-Downloader or the OSCDL-Mass-Downloader
For when ya just aint patient no mo'.
[*Go support the actual OSC team! They're the entire reason this thing exists. Maybe donate a dolla or two? Hm?*](https://oscwii.org/)
I made this while I was bored, and, having access to GPT, I asked it to make this. Took a lot of trial and error.
I also made this because, well, the OSCDL current revision doesn't have it. Code will be deprecated and archived once it does. 
Let's get to it.

# OSCMD Instructions Manual 
(for yeh bloody idiots)

Read and think.
Script downloads from JSON, extracts for you, and onto whatever destination you want.
---

## Requirements

Before starting, make sure you have:

* **Python 3.x** ([Download here](https://www.python.org/downloads/))  
* **Command Prompt** (Windows built-in)  
* **Windows 10+**  
* **A browser**  
* **WinRAR** (for manual zip checking, optional)  
* **An already set-up Wii Homebrew SD card/USB** with the apps folder ready  

---

## Step 1 — Install Python and Required Modules

1. Install Python if you don’t already have it. During installation, check **“Add Python to PATH”**.  
2. Open Command Prompt and install required Python packages from  requirements.txt :
pip install -r requirements.txt
    

---

## Step 2 — Download the JSON File

1. Go to [OSC API v3](https://hbb1.oscwii.org/api/v3/contents) (or v4 if v3 is deprecated).
2. Save the page as a  .json  file anywhere on your PC. Example:
C:\Users\You\Downloads\hbb_contents.json
<img width="754" height="286" alt="image" src="https://github.com/user-attachments/assets/ab159839-2687-4120-93a3-1708cc4c6608" />

> ✅ Note: The location of this file is flexible, just remember the path.

---

## Step 3 — Edit the Python Script

1. Open the  .py  script in a text editor (Notepad, VSCode, etc.).
2. Find the line:
JSON_FILE = "goes here bitch"  # path to your local JSON
3. Replace it with the full path to your downloaded JSON, for example:
JSON_FILE = r"C:\Users\You\Downloads\hbb_contents.json"
   

.⚠️ **Important:**
.
. * Use **raw strings** ( r"..." ) or **double backslashes** ( C:\\Users\\You\\Downloads\\file.json ).
. * Single backslashes ( C:\Users\You\Downloads\file.json ) **will not work** in Python.

4. Save the file.

---

## Step 4 — Run the Script

1. Open Command Prompt.
2. Navigate to the folder where the  .py  script is located:
cd C:\path\to\script
3. Run the script:
python script_name.py
4. The script will ask you:
Enter the full path where you want the folders to go (e.g. E:\apps):
* Enter the path to your target apps folder on your PC (or SD card folder).
* **Example:**   
E:\\apps
or
r"E:\apps"
   
. ⚠️ Do **not** type  E:\apps  — Python interprets  \a  as an escape sequence.

5. The script will then:

   * Download all zips from the JSON.
   * Extract each zip into a temporary folder.
   * Delete the zip files after extraction.
   * Move all extracted folders to the target folder.
   * Flatten any duplicate-named folders and remove extra nested  apps  folders.

---

## Step 5 — Verify the Folder Structure

After the script finishes:

* Check your target folder (e.g.,  E:\apps ).
* All apps should now be directly in the folder, no nested duplicates, no leftover zips.
* Folder structure should look like:
JUST AN EXAMPLE!!!
   
E:\apps\app1
E:\apps\app2
E:\apps\app3
...


. ✅ Each app folder contains the proper files ready for your SD card.

---

## Step 6 — Copy to SD Card
**NOT NECESSARY IF YOUR TARGET DEST IS YOUR SD/USB!!**
1. Open your SD card’s  apps  folder.
2. Drag all the folders from your PC target folder into the SD card  apps  folder.
3. If prompted about duplicates, the script already flattened most, so you can safely overwrite or merge.

---

## Step 7 — Done

* Your SD card should now have **all downloaded apps ready for Wii Homebrew**.
* If you encounter any missing apps or errors, check the  JSON_FILE  path and rerun the script.

---

### Optional Notes

* You don’t need to manually extract zips anymore — the script does it automatically.
* If you run the script multiple times, it will **merge new apps** and handle duplicate folders automatically.
* Keep your  downloads  folder clean — the script reuses it as a temporary extraction location.

---

### Tips for Windows Paths

* Always use **double backslashes**:  E:\\apps 
* Or use a **raw string**:  r"E:\apps" 
* Never use single backslashes like  E:\apps  — Python will misinterpret it.



----random shit----

boy oh boy i sure do hope my rep shows up on google
the mischevious search engine of very selective words (it only shows up on OSCDL)
