from dataclasses import dataclass
from typing import List

@dataclass(eq=False)
class Item:
    """Base class for spotify objects"""
    id:str
    name:str

    def __eq__(self, other) -> bool:
        """Items are only compared if they have the same id"""
        return self.id == other.id    

@dataclass(eq=False)
class PlaylistItem(Item):
    """Container for playlist information"""
    owner:str
    length:int
    version:str


@dataclass(eq=False)
class TrackItem(Item):
    """A container for relavent track information"""
    duration:int
    dance:float
    tempo:float
    energy:float
    artist_id:str
    album_id:str
    playlist_id:str

    def same_artist_as(self,other) -> bool:
        return self.artist_id == other.artist.id
    
    def same_album_as(self,other) -> bool:
        return self.album_id == other.album_id

@dataclass(eq=False)
class AlbumItem(Item):
    """A container for relavent album information"""
    release_date:str
    artist_id:str

@dataclass(eq=False)
class ArtistItem(Item):
    """A container for relavent artist information"""
    genre:str
