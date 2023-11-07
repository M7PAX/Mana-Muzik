import os
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TPE1, TRCK, TALB

Path ="C:/Users/niksu/Music/Juice WRLD/70's.mp3"

def GetTitle(FilePath):
    try:
        audio = EasyID3(FilePath)
        title = audio['title'][0]
        return print(title)
    except Exception as e:
        #print(f"Error: {e}")
        return None

def GetArtist(FilePath):
    try:
        audio = EasyID3(FilePath)
        artist = audio['artist'][0]
        return print(artist)
    except Exception as e:
        #print(f"Error: {e}")
        return None

def TitleChange(FilePath,NewTitle):
        try:
            audio = EasyID3(FilePath)
        except mutagen.id3.ID3NoHeaderError:
            audio = mutagen.File(FilePath, easy=True)
            audio.add_tags()

        audio['title'] = NewTitle
        audio.save(FilePath)
        changed = EasyID3(FilePath)
            
def ArtistChange(FilePath,NewArtist):
            try:
                audio = EasyID3(FilePath)
            except mutagen.id3.ID3NoHeaderError:
                audio = mutagen.File(FilePath, easy=True)
                audio.add_tags()

            audio['artist'] = NewArtist
            audio.save(FilePath)
            changed = EasyID3(FilePath)

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

GetArtist(Path)