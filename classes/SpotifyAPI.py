import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from classes import Items
from typing import List



class SpotifyAPI():
    """Controls functionality for spotipy"""

    def __init__(self) -> None:
        self.ID = cred.clientID
        self.SECRET = cred.clientSecret
        self.URI = cred.redirectURL
        self.SCOPE = "playlist-read-private user-read-private"

        self.auth_manager = SpotifyOAuth(
            client_id=self.ID,
            client_secret=self.SECRET,
            redirect_uri=self.URI,
            scope=self.SCOPE)

        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_playlists(self) -> List[Items.PlaylistItem]:
        """Gets the playlist items"""
        
        playlist_list = self.sp.current_user_playlists()['items']
        return [Items.PlaylistItem(playlist) for playlist in playlist_list]

    def get_tracks(self,playlist:Items.PlaylistItem) -> List[Items.TrackItem]:
        """Gets all tracks in a playlist"""

        #Gets first 100 items from a playlist
        results = self.sp.playlist_items(playlist.id)
        tracks = results['items']
        
        #Loops into it reaches the end of the playlist
        while results['next']:
            #Looks at the next 100 items in the playlist
            results = self.sp.next(results)
            #extends the list to include the extra items
            tracks.extend(results['items'])
    
        track_items = []
        #Goes through list of tracks and generates track item objects
        for i,track in enumerate(tracks):
            print(f"Processing Track {i+1}/{len(tracks)}")

            track_features = self.sp.audio_features(track['track']['id'])
            track_items.append(Items.TrackItem(track,track_features,playlist.id))
        
        return track_items
    
    def get_albums(self,track_list:List[Items.TrackItem]) -> List[Items.AlbumItem]:
        """Gets the albums from a list of tracks"""
        albums = []
        for i,track in enumerate(track_list):
            print(f"Processing album {i+1}/{len(track_list)}")
            album = self.sp.album(track.album_id)
            albums.append(Items.AlbumItem(album,track.artist_id))
        return albums

    def get_artist(self,track_list:List[Items.TrackItem]) -> List[Items.ArtistItem]:
        """Gets the artist from a list of tracks"""
        artists = []
        for track in track_list:
            artist = self.sp.artist(track.artist_id)
            artists.append(Items.ArtistItem(artist))
        return artists