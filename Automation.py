import os
import eyed3
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TPE1, TRCK, TALB

MusicFolder ='C:/Users/niksu/Music/Juice WRLD'
Artist = "Juice WRLD"
files = os.listdir(MusicFolder)
#file, title, artist, album, tn, genre, year, comment

def TitleAuto():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)

            try:
                audio = EasyID3(file_path)
            except mutagen.id3.ID3NoHeaderError:
                audio = mutagen.File(file_path, easy=True)
                audio.add_tags()

            type(audio)
            title = file[:-4]
            audio['title'] = title
            audio.save()

def ArtistAuto():
    #artist = TPE1(encoding=3, text=Artist)
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)

            try:
                audio = EasyID3(file_path)
            except mutagen.id3.ID3NoHeaderError:
                audio = mutagen.File(file_path, easy=True)
                audio.add_tags()

            type(audio)
            audio['artist'] = Artist
            audio.save()


def RemoveAlbum():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            audio = ID3(file_path)
            if 'TALB' in audio:
                del audio['TALB']
            audio.save()

def RemoveTN():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            audio = ID3(file_path)
            if 'TRCK' in audio:
                del audio['TRCK']
            audio.save()

def RemoveGenre():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            audio = eyed3.load(file_path)
            audio.tag.genre = None
            audio.tag.save()

def RemoveYear():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            audio = ID3(file_path)
            if 'TDRC' in audio:
                del audio['TDRC']
            audio.save()

def RemoveComment():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            audio = eyed3.load(file_path)
            audio.tag.comments.set('')
            audio.tag.save()


# TitleAuto()
# ArtistAuto()

# RemoveAlbum()
# RemoveTN()
# RemoveGenre()
# RemoveYear()
# RemoveComment()