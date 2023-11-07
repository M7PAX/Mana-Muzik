import os
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TPE1, TRCK, TALB

MusicFolder ='C:/Users/niksu/Music/Juice WRLD'
Artist = "Juice WRLD"
files = os.listdir(MusicFolder)

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
            audio.save(file_path, v1=2)
            changed = EasyID3(file_path)
            
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
            audio.save(file_path, v1=2)
            changed = EasyID3(file_path)

def RemoveTN():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            audio = ID3(file_path)
            audio.delall('TRCK')
            audio.save()

def RemoveAlbum():
    for file in files:
        if file.endswith(".mp3"):
            file_path = os.path.join(MusicFolder, file)
            audio = ID3(file_path)
            if 'TALB' in audio:
                del audio['TALB']
            audio.save()

TitleAuto()
ArtistAuto()
RemoveTN()
RemoveAlbum()