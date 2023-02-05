from classes.Database import Database
from classes.DataManager import DataManager
from classes.FigureGenerator import FigureGenerator

#Columns to be looked at
columns = ["Dance","Tempo","Energy","PlaylistID"]

#Getting the data from database
db = Database("Database.db")

songs = DataManager(db.select_all("Songs"))
playlists = DataManager(db.select_all("Playlists"))
albums = DataManager(db.select_all("Albums"))
artists = DataManager(db.select_all("Artists"))

gen = FigureGenerator(songs,playlists,albums,artists)

#gen.dance_energy()
gen.avg_genre()
#gen.avg_bar()