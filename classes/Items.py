from dataclasses import dataclass
from typing import List

@dataclass
class PlaylistItem:
    """Container for playlist information"""
    id:str
    name:str
    owner:str
    length:int
    version:str

@dataclass
class TrackItem:
    """A container for relavent track information"""
    id:str
    name:str
    duration:int
    dance:float
    tempo:float
    energy:float
    artist_id:str
    album_id:str
    playlist_id:str

@dataclass
class AlbumItem:
    """A container for relavent album information"""
    id:str
    name:str
    release_date:str
    artist_id:str

@dataclass
class ArtistItem:
    """A container for relavent artist information"""
    id:str
    name:str
    genre:List[str]
