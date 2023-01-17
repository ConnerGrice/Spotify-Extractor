import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from classes import Items
from typing import List



class SpotifyAPI():
    """Controls functionality for spotipy"""

    def __init__(self) -> None:
        #Gets info for auth manager
        self.ID = cred.clientID
        self.SECRET = cred.clientSecret
        self.URI = cred.redirectURL
        self.SCOPE = "playlist-read-private user-read-private"

        #Generates manager
        self.auth_manager = SpotifyOAuth(
            client_id=self.ID,
            client_secret=self.SECRET,
            redirect_uri=self.URI,
            scope=self.SCOPE)

        #Establishes connection to Spotify
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_playlists(self) -> List[Items.PlaylistItem]:
        """Gets the playlist items"""
        
        #Gets list of playlists
        playlist_list = self.sp.current_user_playlists()['items']

        output = []
        #Loops through playlists and extracts wanted information
        for playlist in playlist_list:
            id = playlist['id']
            name = playlist['name']
            owner = playlist['owner']['display_name']
            length = playlist['tracks']['total']
            version = playlist['snapshot_id']

            #Puts info into playlist dataclass
            output.append(Items.PlaylistItem(id,name,owner,length,version))

        return output

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

            #Gets extra audio data
            track_features = self.sp.audio_features(track['track']['id'])

            id = track['track']['id']
            name = track['track']['name']
            duration = track['track']['duration_ms']
            dance = track_features[0]['danceability']
            tempo = track_features[0]['tempo']
            energy = track_features[0]['energy']
            artist_id = track['track']['artists'][0]['id']
            album_id = track['track']['album']['id']

            track_item = Items.TrackItem(
                id,
                name,
                duration,
                dance,
                tempo,
                energy,
                artist_id,
                album_id,
                playlist.id
                )

            track_items.append(track_item)
        
        return track_items
    
    def get_albums(self,track_list:List[Items.TrackItem]) -> List[Items.AlbumItem]:
        """Gets the albums from a list of tracks"""
        albums = []

        #Loops through track list and gets corresponding album
        for i,track in enumerate(track_list):
            print(f"Processing album {i+1}/{len(track_list)}")
            album = self.sp.album(track.album_id)

            id = album['id']
            name = album['name']
            release_date = album['release_date']
            artist_id = track.artist_id
            
            album_item = Items.AlbumItem(id,name,release_date,artist_id)
            albums.append(album_item)
        return albums

    def get_artists(self,track_list:List[Items.TrackItem]) -> List[Items.ArtistItem]:
        """Gets the artist from a list of tracks"""
        artists = []

        #Loops through track list and gets corresponding artist
        for i,track in enumerate(track_list):
            print(f"Processing artist {i+1}/{len(track_list)}")
            artist = self.sp.artist(track.artist_id)

            id = artist['id']
            name = artist['name']
            genres = artist['genres']

            artist_item = Items.ArtistItem(id,name,genres)
            artists.append(artist_item)
        return artists