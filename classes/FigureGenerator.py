from classes.DataManager import DataManager
from bokeh.plotting import figure,output_file,show
from bokeh.models import ColumnDataSource,CheckboxGroup,CustomJS,HoverTool,Range1d
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

        self.green = "#1DB954"
        self.black = "#191414"
        self.white = "#FFFFFF"

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

        artist_names = self.songs.column["ArtistID"]
        artist_names = artist_names.map(self.songs.map_of(self.artists.column["Name"],"ArtistID"))

        
        #Joining data together
        data = pd.concat([dance,energy,names,song_name,artist_names],axis=1)

        hover = HoverTool(tooltips=[
            ("Name","@Name"),
            ("Artist","@ArtistID"),
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
            Name=[],
            ArtistID=[]
            ))

        #Formatting figure
        p = figure(title= "Dance vs Energy",
                   x_axis_label="Dance",
                   y_axis_label="Energy",
                   width = 400,
                   height = 400,
                   background_fill_color=self.black,
                   x_range = Range1d(0,1),
                   y_range = Range1d(0,1),
                   tools=[hover])
        
        p.grid.grid_line_color = None
        p.axis.axis_label_text_font_style = 'bold'
        
        #Plotting points
        p.scatter(x="Dance",
                  y="Energy",
                  source=filtered,
                  color=self.green)

        #Generating playlist check boxes
        check_boxes = CheckboxGroup(labels=labels,active=[],height=200)

        #Called when check boxes are clicked
        callback = CustomJS(args=dict(source=source,filtered=filtered),code="""
            var data = source.data;
            var f_data = filtered.data;

            var new_dance = [];
            var new_energy = [];
            var new_label = [];
            var new_playlist = [];
            var new_name = [];
            var new_artist = [];

            const active = cb_obj.active;
            
            var dance = data['Dance'];
            var energy = data['Energy'];
            var labels = data['Playlist_activeID'];
            var playlist = data['PlaylistID'];
            var name = data['Name'];
            var artist = data['ArtistID'];

            for (let i=0;i<dance.length;i++){
                for (let j=0;j<active.length;j++){
                    if (labels[i] == active[j]){
                        new_dance.push(dance[i]);
                        new_energy.push(energy[i]);
                        new_label.push(labels[i]);
                        new_playlist.push(playlist[i]);
                        new_name.push(name[i]);
                        new_artist.push(artist[i])

                    }
                }
            }   

            f_data['Dance'] = new_dance;
            f_data['Energy'] = new_energy;
            f_data['Playlist_activeID'] = new_label;
            f_data['PlaylistID'] = new_playlist;
            f_data['Name'] = new_name;
            f_data['ArtistID'] = new_artist;

            filtered.change.emit();
        """)
        check_boxes.js_on_change("active",callback)
        
        show(row(check_boxes,p))

    def get_genres(self,genres_series:pd.Series) -> pd.Series:
        """Converts string of genres for each song into a list"""
        final = []
        for song,genres in genres_series.items():
            genres = genres.strip("[]")
            genres_list = genres.split(",")
            out = []
            for item in genres_list:
                out.append(item.strip(" ''"))
            
            final.append(tuple([song,out]))
        
        index,values = zip(*final)
        return pd.Series(values,index,name="Genres")


    def avg_genre(self) -> pd.Series:
        """Gets a series of the playlists and thier average genres (mode)"""
        
        #Gets genres and maps then to each song
        artist_genre = self.songs.column["ArtistID"]
        artist_genre = artist_genre.map(self.songs.map_of(self.artists.column["Genre"],"ArtistID"))

        #Gets genres in the form of a series of lists
        genres = self.get_genres(artist_genre)

        #Get playlist ids
        playlists = self.songs.column["PlaylistID"]

        #Combine playlist ids with genres
        data = pd.concat([playlists,genres],axis=1)
        
        #Groups genres into playlists and finds the mode
        data = data.explode("Genres")
        genre_mode = data.groupby("PlaylistID")["Genres"].agg(pd.Series.mode)
        
        return genre_mode
            



    def avg_bar(self):
        song_df = self.songs.df

        print(song_df.groupby("PlaylistID").agg(pd.Series.mode))

        