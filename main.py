# ask user for their top level songs directory
import logging
import os

import archive

logging.basicConfig(filename='./log.txt', encoding='utf-8', level=logging.WARNING, filemode='w')

# top level directories for songs and zips
with open("config.txt", "r") as f:
    song_tld = f.readline().strip()
    zip_tld = f.readline().strip()
    print("Song directory: " + song_tld)
    print("Zip directory: " + zip_tld)

    prompt = input("Is this correct? (y/n): ")
    if prompt.lower() != "y":
        print("Please edit config.txt and try again.")
        exit(-1)

# store dictionary of songs + the corresponding directories by recursively going to the lowest level of song_tld
song_dirs = dict()
for root, dirs, files in os.walk(song_tld):
    if "song.ogg" in files or "video.mp4" in files or "song.ini" in files or "album.png" in files or True in (
            ".chart" in f for f in files):
        name = os.path.basename(root)

        # check if there is a conflicting directory name in the song_dirs dictionary
        if name in song_dirs:
            # if there is, check if the conflicting directory is a subdirectory of the current directory
            if True in ((os.path.commonpath([root, i]) == song_dirs[name]) for i in song_dirs[name]):
                # if it is, skip
                continue
            # if it is not, then append the current directory to the list of directories for the song and move on
            song_dirs[name].append(root)
            continue

        song_dirs[name] = [root]

zip_dirs = dict()
# initialize zip_dirs with the same keys as song_dirs but with empty lists as values
for key in song_dirs:
    zip_dirs[key] = []

# resursively go to the lowest level of zip_tld to see if the directories in the zip, rar, or 7z files match the song names in song_dirs,
# and save these matches in zip_dirs
for root, dirs, files in os.walk(zip_tld):
    for name in files:
        # check if the file is a valid file
        try:
            for aroot, adirs, afiles in archive.walk(os.path.join(root, name)):
                if aroot in zip_dirs:
                    zip_dirs[aroot].append(os.path.join(root, name, aroot))
                    continue
        except Exception as e:
            logging.warning("Exception: {} \nName:{}".format(e, name))
            continue

# iterate through the keys of song_dirs and zip_dirs
for key, val in song_dirs.items():
    # remove any duplicates in val
    val = list(set(val))

    if len(val) == 0:
        logging.warning("random error. You can probably ignore this.")
        continue

    if len(val) > 1:
        logging.warning("multiple songs with the same name. Skipping '{}'. \nLocated at: {}".format(key, val))
        continue

    # if there are no directories in zip_dirs for the current key, then print a warning and skip
    if len(zip_dirs[key]) == 0:
        logging.warning("Zip files do not contain song. Skipping '{}'. \nLocated at: {}".format(key, val))
        continue

    # if there is more than one directory in zip_dirs for the current key, then print a warning and skip
    if len(zip_dirs[key]) > 1:
        logging.warning("Zip files contain multiple directories for song. Skipping '{}'. \nLocated at: {}".format(key,
                                                                                                                  zip_dirs[
                                                                                                                      key]))
        continue

    # if there is only one directory in zip_dirs for the current key, then replace the song with the files in the directory
    if len(zip_dirs[key]) == 1:
        logging.info("replacing song: " + key)
        src = zip_dirs[key][0]
        dst = val[0]
        logging.info("Copying from {} to {}".format(src, dst))
        if archive.copy(src, dst):
            logging.info("Copy successful")
        else:
            logging.warning("Copy failed for song {}. \nLocated at: {}".format(key, val))
