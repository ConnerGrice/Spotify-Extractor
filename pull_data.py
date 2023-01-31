from classes.Database import Database
import pandas as pd
import numpy as np
from bokeh.plotting import figure,output_file,show
from bokeh.models import ColumnDataSource,CDSView, GroupFilter

#Columns to be looked at
columns = ["Dance","Tempo","Energy","PlaylistID"]

#Getting the data from database
db = Database("Database.db")
data = np.array(db.select_from("Songs",columns))
db.close_table()

#Converting data into the correct format
df = pd.DataFrame(data[:,1:],index=data[:,0],columns=columns)
df = df.apply(pd.to_numeric,errors="ignore")




output_file("output.html")

source = ColumnDataSource(df)
playlists = df.PlaylistID.unique()
view = CDSView(filter=GroupFilter(group=playlists[1],column_name="PlaylistID"))

p = figure(title= "Dance vs Energy",x_axis_label="Dance",y_axis_label="Energy")


p.scatter(x="Dance",y="Energy",source=source,view=view)


show(p)
