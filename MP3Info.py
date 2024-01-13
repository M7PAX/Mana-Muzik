import eyed3
import mutagen
from mutagen.easyid3 import EasyID3

# Path = "C:/Users/niksu/Music/folder/Freddie Dredd - Kill Again.mp3"
# title, artist, cover, album, tn, genre, year, comment

def GetTitle(FilePath):
    try:
        audio = EasyID3(FilePath)
        title = audio["title"][0]
        return str(title)
    except Exception as e:
        # print(f"Error: {e}")
        return None

def GetArtist(FilePath):
    try:
        audio = EasyID3(FilePath)
        artist = audio["artist"][0]
        return str(artist)
    except Exception as e:
        # print(f"Error: {e}")
        return None

#eyeD3
def GetAlbum(FilePath):
    audio = eyed3.load(FilePath)
    album = audio.tag.album

    if not album:
        return None
    return str(album)


def GetTN(FilePath):
    try:
        audio = EasyID3(FilePath)
        tn = audio.get("tracknumber")[0]
        return str(tn)
    except Exception as e:
        # print(f"Error: {e}")
        return None

def GetGenre(FilePath):
    try:
        audio = EasyID3(FilePath)
        genre = audio.get("genre")[0]
        return genre
    except Exception as e:
        # print(f"Error: {e}")
        return None

def GetYear(FilePath):
    try:
        audio = EasyID3(FilePath)
        year = audio.get("date")[0]
        return str(year)
    except Exception as e:
        # print(f"Error: {e}")
        return None

#eyeD3
def GetComment(FilePath):
    try:
        audio = eyed3.load(FilePath)
        comment = audio.tag.comments[0].text
        return str(comment)
    except Exception as e:
        # print(f"Error: {e}")
        return None


def Audio(FilePath):
    try:
        audio = EasyID3(FilePath)
        return audio
    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(FilePath, easy=True)
        audio.add_tags()
        return audio

def TitleChange(FilePath, NewTitle):
    audio = Audio(FilePath)
    EasyID3.RegisterTextKey("title", "TIT2")
    audio["title"] = NewTitle
    audio.save(FilePath)

def ArtistChange(FilePath, NewArtist):
    audio = Audio(FilePath)
    EasyID3.RegisterTextKey("artist", "TPE1")
    audio["artist"] = NewArtist
    audio.save(FilePath)

#eyeD3
def CoverChange(FilePath, NewCover):
    if ('/' in NewCover) == True:
        audio = eyed3.load(FilePath)
        audio.initTag(version=(2, 3, 0))
        if NewCover.startswith('{') and NewCover.endswith('}'):
            NewCover = NewCover[1:-1]
        with open(NewCover, "rb") as image_file:
            imagedata = image_file.read()
        audio.tag.images.set(3, imagedata, "image/jpeg", u"cover")
        audio.tag.save()

def AlbumChange(FilePath, NewAlbum):
    audio = Audio(FilePath)
    EasyID3.RegisterTextKey("album", "TALB")
    audio["album"] = str(NewAlbum)
    audio.save()

def TnChange(FilePath,NewTN):
    audio = Audio(FilePath)
    EasyID3.RegisterTextKey("tracknumber", "TRCK")
    audio["tracknumber"] = str(NewTN)
    audio.save()

def GenreChange(FilePath,NewGenre):
    audio = Audio(FilePath)
    #EasyID3.RegisterTextKey("genre", "")
    audio["genre"] = str(NewGenre)
    audio.save()

def YearChange(FilePath, NewYear):
    audio = Audio(FilePath)
    EasyID3.RegisterTextKey("year", "TDRC")
    audio["year"] = str(NewYear)
    audio.save()

#eyeD3
def CommentChange(FilePath,NewComment):
    audio = eyed3.load(FilePath)
    audio.tag.comments.set(NewComment)
    audio.tag.save()

def RemoveCover(FilePath):
    audio = eyed3.load(FilePath)
    audio.tag.images.remove('')
    audio.tag.save()

# TitleChange(Path, "Kill Again")
# ArtistChange(Path, "Freddie Dredd")
# CoverChange(Path,"C:/Users/niksu/OneDrive/New folder/Attēli/freddie.jpg")
# AlbumChange(Path,"Unreleased")
# TnChange(Path,"7")
# GenreChange(Path,"Rap")
# YearChange(Path, "2020")
# CommentChange(Path,":)")

# print(GetTitle(Path))
# print(GetArtist(Path))
# print(GetAlbum(Path))
# print(GetTN(Path))
# print(GetGenre(Path))
# print(GetYear(Path))
# print(GetComment(Path))