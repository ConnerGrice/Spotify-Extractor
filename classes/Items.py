
class PlaylistItem:
    """A container for relavent playlist information"""
    def __init__(self,playlist:dict) -> None:
        self.id = playlist['id']
        self.name = playlist['name']
        self.owner = playlist['owner']['display_name']
        self.length = playlist['tracks']['total']
        self.version = playlist['snapshot_id']

class TrackItem:
    """A container for relavent track information"""
    def __init__(self,track:dict,track_extra:dict,playlist_id:str) -> None:
        self.id = track['track']['id']
        self.name = track['track']['name']
        self.duration = track['track']['duration_ms']
        self.dance = track_extra[0]['danceability']
        self.tempo = track_extra[0]['tempo']
        self.energy = track_extra[0]['energy']
        self.artist_id = track['track']['artists'][0]['id']
        self.album_id = track['track']['album']['id']
        self.playlist_id = playlist_id
        