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