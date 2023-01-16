import sqlite3
from classes.Tables import Playlists

database = sqlite3.connect("Database.db")

playlist = Playlists(database)

print(playlist.check_exists())

