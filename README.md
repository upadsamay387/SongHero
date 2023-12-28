# SongHero for Clone Hero
This is a simple script to fix any broken song directories for Clone Hero. It searches through your songs directory to compile a list of songs. Then, it looks through a directory full of zip, rar, and 7z files to find the missing songs. Lastly, the songs are extracted back into the songs folder.

## Usage
**BACK UP YOUR SONGS FOLDER BEFORE USING THIS SCRIPT!** This script might overwrite some of your songs. I am not responsible for any lost songs or data.

1. Download Python 3 if you don't have it already.
   * https://www.python.org/downloads/
   - Note: **Double check that Python is added to your PATH.**
     - You can do this by opening a **new** terminal window and typing `python --version` or `python3 --version`. If it gives a "not recognized" error, you need to add it to your PATH.
2. Download 7-Zip and add it to your PATH.
   1. https://www.7-zip.org/download.html
   2. **IMPORTANT**: If you are using Linux, check if you're running a Debian-based distro. If you are, you may need to install *unrar* instead of 7-Zip.
3. Download the script and extract it to a folder.
4. Edit config.txt to point to your songs folder and your folder full of compressed songs.
5. Open a terminal window in the folder you extracted the script to.
6. Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt` to install the required packages.
7. Run the script by typing `python songhero.py` or `python3 songhero.py`.
7. Confirm that the script has the correct folders
8. Wait for the script to finish.
9. Check the logs for any warnings or errors.
10. Enjoy your fixed songs!


## Notes
* This script may overwrite files in the Songs directory.
* This was only tested on Windows 11 with Python 3.11. If you're running into issues, try using Python 3.11 first.
* In its current state, this script might be buggy. There may be a rewrite in the future.
