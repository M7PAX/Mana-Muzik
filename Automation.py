import os
import eyed3
import mutagen
import MP3Info
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

MusicFolder = 'C:/Users/niksu/Music/Juice WRLD'
CoverFolder = 'C:/Users/niksu/OneDrive/New folder/Attēli/Juice WRLD Covers'
Artist = "Juice WRLD"
files = os.listdir(MusicFolder)
covers = os.listdir(CoverFolder)


# file, title, artist, album, tn, genre, year, comment

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


def ArtistAuto():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)

            try:
                audio = EasyID3(file_path)
            except ID3NoHeaderError:
                audio = mutagen.File(file_path, easy=True)
                audio.add_tags()

            audio['artist'] = Artist
            try:
                audio.save()
            except mutagen.MutagenError as e:
                print(f"Error saving artist for {file}: {e}")


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


def RemoveAlbum():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            try:
                audio = ID3(file_path)
                if 'TALB' in audio:
                    del audio['TALB']
                audio.save()
            except Exception as e:
                print(f"Error removing album for {file}: {e}")


def RemoveTN():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            try:
                audio = ID3(file_path)
                if 'TRCK' in audio:
                    del audio['TRCK']
                audio.save()
            except Exception as e:
                print(f"Error removing track number for {file}: {e}")


def RemoveGenre():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            try:
                audio = eyed3.load(file_path)
                audio.tag.genre = None
                audio.tag.save()
            except Exception as e:
                print(f"Error removing genre for {file}: {e}")


def RemoveYear():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            try:
                audio = ID3(file_path)
                if 'TDRC' in audio:
                    del audio['TDRC']
                audio.save()
            except Exception as e:
                print(f"Error removing year for {file}: {e}")


def RemoveComment():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            try:
                audio = eyed3.load(file_path)
                audio.tag.comments.set('')
                audio.tag.save()
            except Exception as e:
                print(f"Error removing comment for {file}: {e}")


def RemoveCover():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            try:
                MP3Info.RemoveCover(file_path)
            except Exception as e:
                print(f"Error removing cover for {file}: {e}")

# CoverAuto()
# TitleAuto()
# ArtistAuto()

# RemoveAlbum()
# RemoveTN()
# RemoveGenre()
# RemoveYear()

# RemoveCover()

# RemoveComment()
