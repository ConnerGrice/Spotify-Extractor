from classes import Tables
from classes import SpotifyAPI
from classes import Items
from dataclasses import astuple
from typing import List

def collect_tracks(playlist:List[Items.PlaylistItem]) -> List[Items.TrackItem]:
    tracks = []
    for playlist in playlist:
        tracks.extend(api.get_tracks(playlist))

    return tracks

def populate(item_list:List[Items.Item],table:Tables.Table) -> None:
    for item in item_list:
        data = astuple(item)
        table.populate_table(data)

db_name = "Database.db"

playlist_table = Tables.Playlists(db_name)
artist_table = Tables.Artists(db_name)
album_table = Tables.Albums(db_name)
track_table = Tables.Songs(db_name)

playlist_table.delete_rows()
artist_table.delete_rows()
album_table.delete_rows()
track_table.delete_rows()

api = SpotifyAPI.SpotifyAPI()

playlists = api.get_playlists()

tracks = collect_tracks(playlists)

no_dup_artists = api.remove_dup_artists(tracks)
no_dup_albums = api.remove_dup_albums(tracks)

albums = api.get_albums(no_dup_albums)
artists = api.get_artists(no_dup_artists)

populate(playlists,playlist_table)
populate(tracks,track_table)
populate(albums,album_table)
populate(artists,artist_table)

