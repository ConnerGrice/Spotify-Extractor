from classes.Database import Database
from classes.SpotifyAPI import SpotifyAPI
from classes.Items import PlaylistItem
import pandas as pd
import numpy as np
#Initialize database and api
db = Database("Database.db")
api = SpotifyAPI()

#Gets a set of version codes from the database
old_playlists = np.array(db.select_from("Playlists",["Version"]))
old_playlists = pd.Series(old_playlists[:,1],index=old_playlists[:,0],name="Version")

#Gets a set of version codes from spotify
new_playlists = api.get_playlists()
new_playlist_ids = [item.id for item in new_playlists]
new_playlist_versions = [item.version for item in new_playlists]
new_playlists_s = pd.Series(new_playlist_versions,name="Versions",index=new_playlist_ids)

print(old_playlists.head())
print(new_playlists.head())

#Gets the IDs of the playlists that have been added/modified
different_playlists = new_playlists_s.isin(old_playlists)
different_playlists = different_playlists.loc[different_playlists == False].index

print(different_playlists)

#Goes through playlists and searches them in the database
for id in different_playlists:
    playlist = db.select_single_id("Playlists",id)
    if playlist:
        playlist_id,name,owner,length,version = playlist
        playlist_item = PlaylistItem(playlist_id,name,owner,length,version)
        print(playlist_id,name,owner,length,version)

