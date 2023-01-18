from classes import Tables
from classes import SpotifyAPI
from classes import Items
from dataclasses import astuple
from typing import List

def collect_tracks(playlist:List[Items.PlaylistItem]) -> List[Items.TrackItem]:
    """Collects tracks from a list of playlists"""
    tracks = []
    for playlist in playlist:
        tracks.extend(api.get_tracks(playlist))

    return tracks

def populate(item_list:List[Items.Item],table:Tables.Table) -> None:
    """Inserts data into a given table object"""
    data = [astuple(item) for item in item_list]
    table.populate_table(data)

def populate_close(table:Tables.Table,data:List[Items.Item]) -> None:
    """Removes any existing rows before populating the table, then closing the connection"""
    table.delete_rows()
    populate(data,table)
    table.close_table()

#Initialize API controller
api = SpotifyAPI.SpotifyAPI()

#Gets a list of users playlists
playlists = api.get_playlists()

#Gets all tracks from each playlist
tracks = collect_tracks(playlists)

#Cleans the data to remove duplicates
no_dup_artists = api.remove_dup_artists(tracks)
no_dup_albums = api.remove_dup_albums(tracks)

#Gets a list of albums and artists from the tracks in users playlists
albums = api.get_albums(no_dup_albums)
artists = api.get_artists(no_dup_artists)

#Declares the name of the database
db_name = "Database.db"

#Initializes and populates the playlists table
playlist_table = Tables.Playlists(db_name)
populate_close(playlist_table,playlists)

#Initializes and populates the tracks table
track_table = Tables.Songs(db_name)
populate_close(track_table,tracks)

#Initialize and populates the albums table
album_table = Tables.Albums(db_name)
populate_close(album_table,albums)

#Initialize and populates the artists table
artist_table = Tables.Artists(db_name)
populate_close(artist_table,artists)
