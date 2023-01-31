from classes.Database import Database
from classes.SpotifyAPI import SpotifyAPI
from classes import Utils
import pandas as pd
import numpy as np

#Initialize database and api
db = Database("Database.db")
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
print(difference)

#Goes through each playlist that has changed
for i,j in zip(difference.index,changes):
    #If the playlist was removed
    if not j:
        #Deletes songs that are inside playlist
        Utils.delete_songs(db,i)

        #Deletes playlist entry
        db.delete_with_contraint("Playlists","PlaylistID",[(i,)])

        #Deletes artist or album entries if there is no song connected to them
        Utils.cascade_delete_from_songs(db,"Artists")
        Utils.cascade_delete_from_songs(db,"Albums")
    elif j:
        #Gets info on updated playlist and puts it into the database
        playlist = api.get_single_playlist(i)
        db.insert_single("Playlists",playlist)

        #Gets a list of all the songs and thier info and puts them into the database
        tracks = api.get_tracks(playlist)
        db.insert_many("Songs",tracks)

        #Removes any dluplicate artists and ablums
        no_dup_artists = api.remove_dup_artists(tracks)
        no_dup_albums = api.remove_dup_albums(tracks)

        #Gets a list of albums and artists from the tracks in playlist
        albums = api.get_albums(no_dup_albums)
        artists = api.get_artists(no_dup_artists)

        #Updates database with new albums and artists
        db.insert_many("Albums",albums)
        db.insert_many("Artists",artists)

db.close_table()