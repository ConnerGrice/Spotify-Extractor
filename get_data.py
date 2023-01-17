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
    data = [astuple(item) for item in item_list]
    table.populate_table(data)

db_name = "Database.db"



api = SpotifyAPI.SpotifyAPI()

playlists = api.get_playlists()

tracks = collect_tracks(playlists[0:1])

no_dup_artists = api.remove_dup_artists(tracks)
no_dup_albums = api.remove_dup_albums(tracks)

albums = api.get_albums(no_dup_albums)
artists = api.get_artists(no_dup_artists)

playlist_table = Tables.Playlists(db_name)
playlist_table.delete_rows()
populate(playlists,playlist_table)
playlist_table.close_table()


track_table = Tables.Songs(db_name)
track_table.delete_rows()
populate(tracks,track_table)
track_table.close_table()

album_table = Tables.Albums(db_name)
album_table.delete_rows()
populate(albums,album_table)
album_table.close_table()


artist_table = Tables.Artists(db_name)
artist_table.delete_rows()
populate(artists,artist_table)
artist_table.close_table()
