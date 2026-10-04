import os
import shutil
import subprocess
import sys
import tkinter.filedialog as fd
from tkinter import messagebox
from PIL import Image


def AutoClick():
  messagebox.showinfo(message="Coming soon! Lil Bibby soon!")


def Info():
  messagebox.showinfo(
      title="Info",
      message="""Tutorial and Instructions

1. Locate the "Music Directory" option in the top bar and add a directory, which is a folder with a folder of each artist or a folder of your mp3 files.
2. Use the "Folders" drop-down menu to select the specific folder you want to work with.
3. In the listbox, choose the desired song that you want to edit. Begin the editing process, making any changes needed. Be sure to save your modifications when done.
Note: To update the album cover, click "Open Cover" to select an image (supporting jpg, jpeg, and png formats).

Bugs:
In case the cover change doesn't work correctly, try removing the existing cover and then attempt to set it again.

These guidelines should help you navigate through the program smoothly. If you encounter any issues feel free to reach out on GitHub at M7PAX.
""",
  )


def GetMusicFolders(path):
  if not path or not os.path.isdir(path):
    return []
  try:
    contents = os.listdir(path)
    music_folders = [
        item for item in contents if os.path.isdir(os.path.join(path, item))
    ]
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


def SystemAskDirectory(title="Select Folder", initialdir=None):
  """Uses the operating system's native file explorer dialog to select a directory."""
  if not initialdir or not os.path.exists(initialdir):
    initialdir = os.path.expanduser("~")

  if sys.platform.startswith("linux"):
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").upper()

    # KDE Plasma / kdialog (Dolphin native dialog)
    if ("KDE" in desktop or shutil.which("kdialog")) and shutil.which(
        "kdialog"
    ):
      try:
        cmd = [
            "kdialog",
            "--title",
            title,
            "--getexistingdirectory",
            str(initialdir),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
          path = res.stdout.strip()
          if path:
            return path
        else:
          return ""
      except Exception:
        pass

    # GNOME / GTK / zenity
    if shutil.which("zenity"):
      try:
        cmd = [
            "zenity",
            "--file-selection",
            "--directory",
            f"--title={title}",
            f"--filename={initialdir}/",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
          path = res.stdout.strip()
          if path:
            return path
        else:
          return ""
      except Exception:
        pass

  return fd.askdirectory(title=title, initialdir=initialdir)


def SystemAskOpenFile(title="Select File", initialdir=None, filetypes=None):
  """Uses the operating system's native file explorer dialog to open a file."""
  if not initialdir or not os.path.exists(initialdir):
    initialdir = os.path.expanduser("~")

  if sys.platform.startswith("linux"):
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").upper()

    # KDE Plasma / kdialog
    if ("KDE" in desktop or shutil.which("kdialog")) and shutil.which(
        "kdialog"
    ):
      try:
        filter_str = (
            "*.jpg *.jpeg *.png *.webp *.bmp *.gif|Image Files"
            if filetypes
            else "*"
        )
        cmd = [
            "kdialog",
            "--title",
            title,
            "--getopenfilename",
            str(initialdir),
            filter_str,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
          path = res.stdout.strip()
          if path:
            return path
        else:
          return ""
      except Exception:
        pass

    # GNOME / GTK / zenity
    if shutil.which("zenity"):
      try:
        cmd = ["zenity", "--file-selection", f"--title={title}"]
        if initialdir:
          cmd.append(f"--filename={initialdir}/")
        if filetypes:
          cmd.append(
              "--file-filter=Image Files (jpg, png, webp, gif) | *.jpg *.jpeg"
              " *.png *.webp *.bmp *.gif"
          )
          cmd.append("--file-filter=All Files | *")
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
          path = res.stdout.strip()
          if path:
            return path
        else:
          return ""
      except Exception:
        pass

  return fd.askopenfilename(
      title=title, initialdir=initialdir, filetypes=filetypes
  )


def OpenInSystemExplorer(path):
  """Opens a file or directory in the system's native file explorer (e.g. Dolphin, Nautilus, Explorer)."""
  if not path or not os.path.exists(path):
    return

  try:
    if sys.platform == "win32":
      if os.path.isfile(path):
        subprocess.run(["explorer", f"/select,{os.path.normpath(path)}"])
      else:
        os.startfile(os.path.normpath(path))
    elif sys.platform == "darwin":
      if os.path.isfile(path):
        subprocess.run(["open", "-R", path])
      else:
        subprocess.run(["open", path])
    else:
      # Linux
      if os.path.isfile(path):
        if shutil.which("dolphin"):
          subprocess.Popen(["dolphin", "--select", path])
          return
        folder = os.path.dirname(path)
        subprocess.Popen(["xdg-open", folder])
      else:
        subprocess.Popen(["xdg-open", path])
  except Exception as e:
    print(f"Error opening system file explorer: {e}")
