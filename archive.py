# archive needs 3 functions:
# it must walk
# it must open a zip, rar, or 7z file and navigate to a given directory
# it must copy to a destination directory
import os
import zipfile

import rarfile
from py7zr import py7zr


# src is the source path within a zip, rar, or 7z file
# dst is the destination path outside of an archive

# adapted from https://stackoverflow.com/questions/66181180/perform-an-os-walk-through-a-zip-compressed-file-using-the-zipfile-module
# Mimic os.walk() function for zipfiles
def walk(filename: str):
    infolist = None
    is_sz = False

    if ".zip" in filename:
        # Open zip file
        file = zipfile.ZipFile(filename)
        infolist = file.infolist()

    elif ".rar" in filename:
        # Open rar file
        rfile = rarfile.RarFile(filename)
        infolist = rfile.infolist()

    elif ".7z" in filename:
        # Open 7z file
        szfile = py7zr.SevenZipFile(filename)
        infolist = szfile.list()
        is_sz = True

    if infolist is None:
        raise Exception("File is not a zip, rar, or 7z file")

    # Initialize database
    dlistdb = {}

    # Walk through zip file information list
    for info in infolist:

        if (is_sz and info.is_directory) or ((not is_sz) and info.is_dir()):
            path = os.path.dirname(os.path.dirname(info.filename).rstrip('/'))
            file = os.path.basename(os.path.dirname(info.filename).rstrip('/'))
            if path in dlistdb:
                dlistdb[path][0].append(file)
            else:
                dlistdb[path] = [[file], []]
        else:
            path = os.path.dirname(info.filename)
            file = os.path.basename(info.filename)
            if path in dlistdb:
                dlistdb[path][1].append(file)
            else:
                dlistdb[path] = [[], [file]]

    # Convert to os.walk() output format
    dlist = []
    for key in dlistdb.keys():
        dlist.append((key, dlistdb[key][0], dlistdb[key][1]))

    return iter(dlist)


def copy(src: str, dst: str):
    # check if dst is a directory
    if not os.path.isdir(dst):
        return False

    # check if src is a zip, rar, or 7z file
    if ".zip" in src:
        filename = src[:src.find(".zip")] + ".zip"
        member_prefix = src[src.find(".zip") + 5:] + "/"

        with zipfile.ZipFile(filename, 'r') as archive:
            return _copy_helper(archive, dst, member_prefix)

        pass

    elif ".rar" in src:
        filename = src[:src.find(".rar")] + ".rar"
        member_prefix = src[src.find(".rar") + 5:] + "/"

        with rarfile.RarFile(filename, 'r') as file:
            return _copy_helper(file, dst, member_prefix)
        pass

    elif ".7z" in src:
        filename = src[:src.find(".7z")] + ".7z"
        member_prefix = src[src.find(".7z") + 4:] + "/"

        with py7zr.SevenZipFile(filename, 'r') as file:
            return _copy_helper(file, dst, member_prefix, True)
        pass

    else:
        return False

    return True


def _copy_helper(archive, dst, member_prefix, is_sz=False):
    # try:
    if is_sz:
        namelist = archive.getnames()
    else:
        namelist = archive.namelist()

    for file in namelist:
        if "desktop.ini" in file:
            continue
        if file.startswith(member_prefix) and not file.endswith("/"):
            target_path = os.path.join(dst, file[len(member_prefix):])

            with open(target_path, "wb") as f:  # open the output path for writing
                if is_sz:
                    data = archive.read([file])[file].read()
                    archive.reset()
                else:
                    data = archive.read(file)
                f.write(data)  # save the contents of the file in it

    return True  # except Exception as e:  #     logging.warning("Exception: {} \nName:{}".format(e, file))
#     return False
