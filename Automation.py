import os
import MP3Info

MusicFolder = 'C:/Users/niksu/Music/'
CoverFolder = 'C:/Users/niksu/OneDrive/New folder/Attēli/Juice WRLD Covers'
Artist = "Juice WRLD"
files = os.listdir(MusicFolder) if os.path.isdir(MusicFolder) else []
covers = os.listdir(CoverFolder) if os.path.isdir(CoverFolder) else []

# file, title, artist, album, tn, genre, year, comment
AddFunctions = [[MP3Info.ArtistChange, "Juice WRLD"]]
RemoveFunctions = [
    [MP3Info.TitleChange, ""],
    [MP3Info.ArtistChange, ""],
    [MP3Info.AlbumChange, ""],
    [MP3Info.TnChange, ""],
    [MP3Info.GenreChange, ""],
    [MP3Info.YearChange, ""],
    [MP3Info.CommentChange, ""],
]


def _resolve_file(file_path=None):
    if file_path:
        return file_path
    # Check if ManaMuzik GUI is active with a selected file
    try:
        import sys
        for mod_name in ("__main__", "ManaMuzik"):
            mod = sys.modules.get(mod_name)
            if mod and hasattr(mod, "FLClass") and mod.FLClass:
                cur = mod.FLClass.GetCurrentDir()
                if cur and os.path.isfile(cur):
                    return cur
    except Exception:
        pass
    return None


def ChangeAutomation(FunctionList):
    for i in FunctionList:
        for file in files:
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(MusicFolder, file)
                try:
                    i[0](file_path, i[1])
                except Exception as e:
                    print(f"Error updating {file}: {e}")


def TitleAuto():
    for file in files:
        if file.lower().endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            title = os.path.splitext(file)[0]
            try:
                MP3Info.TitleChange(file_path, title)
            except Exception as e:
                print(f"Error saving title for {file}: {e}")


def CoverAuto():
    for file in files:
        if file.lower().endswith(".mp3"):
            file_name = os.path.splitext(file)[0]
            cover_file = file_name + ".png"
            if cover_file in covers:
                file_path = os.path.join(MusicFolder, file)
                cover_path = os.path.join(CoverFolder, cover_file)
                try:
                    MP3Info.CoverChange(file_path, cover_path)
                except Exception as e:
                    print(f"Error changing cover for {file}: {e}")
            else:
                print(f"No cover found for {file}")
