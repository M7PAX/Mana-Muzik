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
        return title
    except Exception as e:
        #print(f"Error: {e}")
        return None

def GetArtist(FilePath):
    try:
        audio = EasyID3(FilePath)
        artist = audio['artist'][0]
        return artist
    except Exception as e:
        #print(f"Error: {e}")
        return None

def GetAlbum(FilePath):
    try:
        audio = EasyID3(FilePath)
        album = audio['album'][0]
        return album
    except Exception as e:
        #print(f"Error: {e}")
        return None
    
def GetTN(FilePath):
    try:
        audio = EasyID3(FilePath)
        TN = audio['tracknumber'][0]
        return TN
    except Exception as e:
        #print(f"Error: {e}")
        return None
    
def GetGenre(FilePath):
    try:
        audio = EasyID3(FilePath)
        genre = audio['genre'][0]
        return genre
    except Exception as e:
        #print(f"Error: {e}")
        return None
    
def GetComment(FilePath):
    try:
        audio = EasyID3(FilePath)
        comment = audio['comment'][0]
        return comment
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

def AlbumChange(FilePath, NewAlbum):
    try:
        audio = EasyID3(FilePath)
    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(FilePath, easy=True)
        audio.add_tags()

    audio['album'] = NewAlbum
    audio.save()

def TNChange(FilePath, NewTN):
    try:
        audio = EasyID3(FilePath)
    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(FilePath, easy=True)
        audio.add_tags()

    audio['tracknumber'] = str(NewTN)
    audio.save()

def GenreChange(FilePath, NewGenre):
    try:
        audio = EasyID3(FilePath)
    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(FilePath, easy=True)
        audio.add_tags()

    audio['genre'] = NewGenre
    audio.save()

def CommentChange(FilePath, NewComment):
    try:
        audio = EasyID3(FilePath)
    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(FilePath, easy=True)
        audio.add_tags()

    audio['comment'] = NewComment
    audio.save()