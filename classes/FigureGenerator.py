from classes.DataManager import DataManager
from bokeh.plotting import figure,output_file,show
from bokeh.models import ColumnDataSource,CheckboxGroup,CustomJS,HoverTool
from bokeh.layouts import row
import pandas as pd

class FigureGenerator:
    """Represents functions that will be used to generate plots"""
    def __init__(self,songs:DataManager,playlists:DataManager,albums:DataManager,artists:DataManager) -> None:
        #Data from database
        self.songs = songs
        self.playlists = playlists
        self.albums = albums
        self.artists = artists

        #Output file for HTML
        output_file("output.html")

    def dance_energy(self):
        """Generates a plot containing all songs and their energy and dance ratings.
        Allows for the user to filter out songs by playlist."""

        #Data to be plotted
        dance = self.songs.column["Dance"]
        energy = self.songs.column["Energy"]
        song_name = self.songs.column["Name"]

        #Mapping playlist IDs to their respective names
        names = self.songs.column["PlaylistID"]
        names = names.map(self.songs.map_of(self.playlists.column["Name"],"PlaylistID"))
        
        #Joining data together
        data = pd.concat([song_name,dance,energy,names],axis=1)

        hover = HoverTool(tooltips=[
            ("Name","@Name"),
            ("Artist","@Artist"),
            ("Playlist", "@PlaylistID")
        ])
        
        #Mapping playlist IDs to the active state given by the checkbox gorup
        labels = list(data.PlaylistID.unique())
        data["Playlist_activeID"] = data["PlaylistID"].map({name:label for (name,label) in zip(labels,range(len(labels)))})
        
        #Defining the data to be used in the plot
        source = ColumnDataSource(data)
        filtered = ColumnDataSource(dict(
            Dance=[],
            Energy=[],
            Playlist_activeID=[],
            PlaylistID=[],

            ))

        p = figure(title= "Dance vs Energy",x_axis_label="Dance",y_axis_label="Energy",tools=[hover])
        p.scatter(x="Dance",y="Energy",source=filtered)

        check_boxes = CheckboxGroup(labels=labels,active=[])

        callback = CustomJS(args=dict(source=source,filtered=filtered),code="""
            var data = source.data;
            var f_data = filtered.data;
            var new_dance = [];
            var new_energy = [];
            var new_label = [];
            var new_playlist = [];

            const active = cb_obj.active;
            
            var dance = data['Dance'];
            var energy = data['Energy'];
            var labels = data['Playlist_activeID'];
            var playlist = data['PlaylistID']

            for (let i=0;i<dance.length;i++){
                for (let j=0;j<active.length;j++){
                    if (labels[i] == active[j]){
                        new_dance.push(dance[i]);
                        new_energy.push(energy[i]);
                        new_label.push(labels[i]);
                        new_playlist.push(playlist[i]);

                    }
                }
            }   

            f_data['Dance'] = new_dance;
            f_data['Energy'] = new_energy;
            f_data['Playlist_activeID'] = new_label;
            f_data['PlaylistID'] = new_playlist;

            filtered.change.emit();
        """)

        check_boxes.js_on_change("active",callback)

        
        show(row(check_boxes,p))

        