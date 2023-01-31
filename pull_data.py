from classes.Database import Database
from classes.DataManager import DataManager
from classes.FigureGenerator import FigureGenerator
import pandas as pd
import numpy as np
from bokeh.plotting import figure,output_file,show
from bokeh.models import ColumnDataSource,CDSView, GroupFilter


#Columns to be looked at
columns = ["Dance","Tempo","Energy","PlaylistID"]

#Getting the data from database
db = Database("Database.db")

songs = DataManager(db.select_all("Songs"))
playlists = DataManager(db.select_all("Playlists"))
albums = DataManager(db.select_all("Albums"))
artists = DataManager(db.select_all("Artists"))

gen = FigureGenerator(songs,playlists,albums,artists)

gen.dance_energy()

# output_file("output.html")

# source = ColumnDataSource(df)
# playlists = df.PlaylistID.unique()
# view = CDSView(filter=GroupFilter(group=playlists[1],column_name="PlaylistID"))

# p = figure(title= "Dance vs Energy",x_axis_label="Dance",y_axis_label="Energy")


# p.scatter(x="Dance",y="Energy",source=source,view=view)


# #show(p)
