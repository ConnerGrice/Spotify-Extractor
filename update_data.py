from classes.Database import Database
from classes.SpotifyAPI import SpotifyAPI
from classes import Utils
import pandas as pd
import numpy as np
#Initialize database and api
db = Database("Database-copy.db")
api = SpotifyAPI()

#Gets a set of version codes from the database
old_playlists = np.array(db.select_from("Playlists",["Version"]))
old_playlists_s = pd.Series(old_playlists[:,1],index=old_playlists[:,0],name="Version")

#Gets a set of version codes from spotify
new_playlists = api.get_playlists()
new_playlist_ids = [item.id for item in new_playlists]
new_playlist_versions = [item.version for item in new_playlists]
new_playlists_s = pd.Series(new_playlist_versions,name="Versions",index=new_playlist_ids)

#Gets a dataframe of all the changes in the playlists
difference = Utils.comparison(old_playlists_s,new_playlists_s)

#Generates a list of bool representing the type of change
#With each element corresponding to the same element in the difference dataframe
changes = Utils.what_change(difference)

#Goes through each playlist that has changed
for i,j in zip(difference.index,changes):
    #If the playlist was removed
    if not j:
        print(i,j)
        #Gets a list of removed songs and converts them into a list of tuples
        removed_songs = Utils.collect_from_ids(db,"Songs","Playlists",f'"{i}"')
        removed_songs = [(s,i) for s in removed_songs]

        db.delete_with_contraint("Playlists","PlaylistID",[(i,)])
        
        #Gets a list of all the artists and albums fromdatabase before deleting songs
        artist_ids_before = set(Utils.get_everything_id(db,"Artists"))
        album_ids_before = set(Utils.get_everything_id(db,"Albums"))

        """DELETES SONGS OF REMOVED PLAYLIST"""
        db.delete_with_contraint_and("Songs",["SongID","PlaylistID"],removed_songs)

        #Get all artists and albumsIDs using remaining songs, removeds dupllicates
        artist_ids_after = set(np.array(db.select_from("Songs",["ArtistID"]))[:,1])
        album_ids_after = set(np.array(db.select_from("Songs",["AlbumID"]))[:,1])

        #Gets a set containing the artists and albums that no longer connect to any songs in the database.
        removed_artists = artist_ids_before - artist_ids_after
        removed_artists = [(a,) for a in removed_artists]

        removed_albums = album_ids_before - album_ids_after
        removed_albums = [(a,) for a in removed_albums]

        print("DELETING")
        db.delete_with_contraint("Artists","ArtistID",removed_artists)
        db.delete_with_contraint("Albums","AlbumID",removed_albums)
        print("DONE")
