import os
from PIL import Image
from tkinter import messagebox


def AutoClick():
    messagebox.showinfo(
        message="Coming soon! Lil Bibby soon!"
    )


def Info():
    messagebox.showinfo(title="Info",
                        message="""Tutorial and Instructions

1. Locate the "Music Directory" option in the top bar and add a directory, which is a folder with a folder of each artist or a folder of your mp3 files.
2. Use the "Folders" drop-down menu to select the specific folder you want to work with.
3. In the listbox, choose the desired song that you want to edit. Begin the editing process, making any changes needed. Be sure to save your modifications when done.
Note: To update the album cover, click "Open Cover" to select an image (supporting jpg, jpeg, and png formats).

Bugs:
In case the cover change doesn't work correctly, try removing the existing cover and then attempt to set it again.

These guidelines should help you navigate through the program smoothly. If you encounter any issues feel free to reach out on GitHub at M7PAX.
""")


def GetMusicFolders(path):
    if not path or not os.path.isdir(path):
        return []
    try:
        contents = os.listdir(path)
        music_folders = [item for item in contents if os.path.isdir(os.path.join(path, item))]
        return sorted(music_folders)
    except Exception:
        return []


def CheckFill(text):
    if text is None:
        text = ""
    return str(text)


def FileChange(file_path, new_file):
    if file_path:
        directory = os.path.dirname(file_path)
        NewPath = os.path.join(directory, new_file + ".mp3")
        os.rename(file_path, NewPath)


def GetImgFormat(img_path):
    try:
        with Image.open(img_path) as img:
            fmt = img.format.lower()
            return "jpeg" if fmt in ("jpg", "jpeg") else fmt
    except Exception as e:
        print(f"Error: {e}")
        return None


def GetFileName(fill_text):
    if not fill_text:
        return ""
    period = fill_text.rfind(".")
    if period != -1:
        fill_text = fill_text[:period]
    return fill_text


def GetDirectoryFile(fill_text):
    return os.path.basename(fill_text)
