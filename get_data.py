from classes import Tables
from classes import SpotifyAPI

db_name = "Database.db"

playlist_table = Tables.Playlists(db_name)
artist_table = Tables.Artists(db_name)
album_table = Tables.Albums(db_name)
song_table = Tables.Songs(db_name)

api = SpotifyAPI.SpotifyAPI()

playlists = api.get_playlists()
tracks = api.get_tracks(playlists[0])
albums = api.get_albums(tracks[0:1])
artists = api.get_artists(tracks[0:10])

print(artists)

