import os
import eyed3
import mutagen
import MP3Info
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

MusicFolder = 'C:/Users/niksu/Music/'
CoverFolder = 'C:/Users/niksu/OneDrive/New folder/Attēli/Juice WRLD Covers'
Artist = "Juice WRLD"
files = os.listdir(MusicFolder)
covers = os.listdir(CoverFolder)

# file, title, artist, album, tn, genre, year, comment
AddFunctions = [[MP3Info.ArtistChange, "Juice WRLD"]]  # , [MP3Info.AlbumChange, "The"], [MP3Info.TnChange, "999"], [MP3Info.GenreChange, "Rap"], [MP3Info.YearChange, "2018"], [MP3Info.CommentChange, ":)"]
RemoveFunctions = [[MP3Info.ArtistChange, ""]]  # , [MP3Info.AlbumChange, ""], [MP3Info.TnChange, ""], [MP3Info.GenreChange, ""], [MP3Info.YearChange, ""], [MP3Info.CommentChange, ""]


def ChangeAutomation(FunctionList):
    for i in FunctionList:
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(MusicFolder, file)

                i[0](file_path, i[1])


def TitleAuto():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)

            try:
                audio = EasyID3(file_path)
            except ID3NoHeaderError:
                audio = mutagen.File(file_path, easy=True)
                audio.add_tags()

            title = file[:-4]
            audio['title'] = title
            try:
                audio.save()
            except mutagen.MutagenError as e:
                print(f"Error saving title for {file}: {e}")


def CoverAuto():
    for file in files:
        if file.endswith(".mp3"):
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


# ChangeAutomation(AddFunctions)
# ChangeAutomation(RemoveFunctions)

# TitleAuto()
# CoverAuto()
