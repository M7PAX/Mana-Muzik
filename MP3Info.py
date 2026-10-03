import os
import Functions
import mutagen
from mutagen.id3 import (
    ID3,
    ID3NoHeaderError,
    TIT2,
    TPE1,
    TALB,
    TRCK,
    TCON,
    TDRC,
    TYER,
    COMM,
    APIC,
)


def _get_id3(FilePath):
    if not FilePath or not os.path.isfile(FilePath):
        return None
    try:
        return ID3(FilePath)
    except ID3NoHeaderError:
        return ID3()
    except Exception:
        try:
            f = mutagen.File(FilePath)
            if f is not None:
                if f.tags is None:
                    f.add_tags()
                return f.tags
        except Exception:
            pass
        return ID3()


def _save_id3(audio, FilePath):
    try:
        audio.save(FilePath, v2_version=3)
    except Exception as e:
        print(f"Error saving metadata to {FilePath}: {e}")


# ========================
# GETTERS
# ========================

def GetTitle(FilePath):
    try:
        audio = ID3(FilePath)
        frames = audio.getall("TIT2")
        if frames and frames[0].text:
            return str(frames[0].text[0])
    except Exception:
        pass
    return ""


def GetArtist(FilePath):
    try:
        audio = ID3(FilePath)
        frames = audio.getall("TPE1")
        if frames and frames[0].text:
            return str(frames[0].text[0])
    except Exception:
        pass
    return ""


def GetAlbum(FilePath):
    try:
        audio = ID3(FilePath)
        frames = audio.getall("TALB")
        if frames and frames[0].text:
            return str(frames[0].text[0])
    except Exception:
        pass
    return ""


def GetTn(FilePath):
    try:
        audio = ID3(FilePath)
        frames = audio.getall("TRCK")
        if frames and frames[0].text:
            return str(frames[0].text[0])
    except Exception:
        pass
    return ""


def GetGenre(FilePath):
    try:
        audio = ID3(FilePath)
        frames = audio.getall("TCON")
        if frames and frames[0].text:
            return str(frames[0].text[0])
    except Exception:
        pass
    return ""


def GetYear(FilePath):
    try:
        audio = ID3(FilePath)
        for key in ("TDRC", "TYER"):
            frames = audio.getall(key)
            if frames and frames[0].text:
                return str(frames[0].text[0])
    except Exception:
        pass
    return ""


def GetComment(FilePath):
    try:
        audio = ID3(FilePath)
        frames = audio.getall("COMM")
        if frames and frames[0].text:
            return str(frames[0].text[0])
    except Exception:
        pass
    return ""


def GetCoverData(FilePath):
    try:
        audio = ID3(FilePath)
        frames = audio.getall("APIC")
        if frames:
            for f in frames:
                if getattr(f, "type", None) == 3 and f.data:
                    return f.data
            for f in frames:
                if f.data:
                    return f.data
    except Exception:
        pass
    return None


def HasCover(FilePath):
    return GetCoverData(FilePath) is not None


# ========================
# EDITORS
# ========================

def EditTitle(FilePath, NewTitle):
    audio = _get_id3(FilePath)
    if audio is None:
        return
    audio.delall("TIT2")
    val = "" if NewTitle is None else str(NewTitle).strip()
    if val:
        audio.add(TIT2(encoding=1, text=[val]))
    _save_id3(audio, FilePath)


def EditArtist(FilePath, NewArtist):
    audio = _get_id3(FilePath)
    if audio is None:
        return
    audio.delall("TPE1")
    val = "" if NewArtist is None else str(NewArtist).strip()
    if val:
        audio.add(TPE1(encoding=1, text=[val]))
    _save_id3(audio, FilePath)


def EditAlbum(FilePath, NewAlbum):
    audio = _get_id3(FilePath)
    if audio is None:
        return
    audio.delall("TALB")
    val = "" if NewAlbum is None else str(NewAlbum).strip()
    if val:
        audio.add(TALB(encoding=1, text=[val]))
    _save_id3(audio, FilePath)


def EditTn(FilePath, NewTN):
    audio = _get_id3(FilePath)
    if audio is None:
        return
    audio.delall("TRCK")
    val = "" if NewTN is None else str(NewTN).strip()
    if val:
        audio.add(TRCK(encoding=1, text=[val]))
    _save_id3(audio, FilePath)


def EditGenre(FilePath, NewGenre):
    audio = _get_id3(FilePath)
    if audio is None:
        return
    audio.delall("TCON")
    val = "" if NewGenre is None else str(NewGenre).strip()
    if val:
        audio.add(TCON(encoding=1, text=[val]))
    _save_id3(audio, FilePath)


def EditYear(FilePath, NewYear):
    audio = _get_id3(FilePath)
    if audio is None:
        return
    audio.delall("TDRC")
    audio.delall("TYER")
    val = "" if NewYear is None else str(NewYear).strip()
    if val:
        audio.add(TDRC(encoding=1, text=[val]))
        audio.add(TYER(encoding=1, text=[val]))
    _save_id3(audio, FilePath)


def EditComment(FilePath, NewComment):
    audio = _get_id3(FilePath)
    if audio is None:
        return
    audio.delall("COMM")
    val = "" if NewComment is None else str(NewComment).strip()
    if val:
        audio.add(COMM(encoding=1, lang="eng", desc="", text=[val]))
    _save_id3(audio, FilePath)


def EditCover(file_path, new_cover):
    if not new_cover or not os.path.isfile(new_cover):
        return
    if (new_cover.startswith('{') and new_cover.endswith('}')) or (new_cover.startswith('"') and new_cover.endswith('"')):
        new_cover = new_cover[1:-1]
    img_format = Functions.GetImgFormat(new_cover)
    if not img_format:
        return

    try:
        with open(new_cover, "rb") as album_art:
            img_data = album_art.read()
    except Exception as e:
        print(f"Error reading cover image {new_cover}: {e}")
        return

    audio = _get_id3(file_path)
    if audio is None:
        return

    audio.delall("APIC")
    mime = "image/jpeg" if img_format in ("jpg", "jpeg") else f"image/{img_format}"
    cover_img = APIC(
        encoding=0,
        mime=mime,
        type=3,  # Front cover
        desc="cover",
        data=img_data,
    )
    audio.add(cover_img)
    _save_id3(audio, file_path)

# ========================
# DELETERS
# ========================

def DeleteTitle(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("TIT2")
        _save_id3(audio, FilePath)


def DeleteArtist(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("TPE1")
        _save_id3(audio, FilePath)


def DeleteAlbum(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("TALB")
        _save_id3(audio, FilePath)


def DeleteTn(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("TRCK")
        _save_id3(audio, FilePath)


def DeleteGenre(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("TCON")
        _save_id3(audio, FilePath)


def DeleteYear(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("TDRC")
        audio.delall("TYER")
        _save_id3(audio, FilePath)


def DeleteComment(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("COMM")
        _save_id3(audio, FilePath)


def DeleteCover(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        audio.delall("APIC")
        _save_id3(audio, FilePath)


def DeleteAllMetadata(FilePath):
    audio = _get_id3(FilePath)
    if audio is not None:
        for tag in ("TIT2", "TPE1", "TALB", "TRCK", "TCON", "TDRC", "TYER", "COMM", "APIC"):
            audio.delall(tag)
        _save_id3(audio, FilePath)
