from classes.DataManager import DataManager
from bokeh.plotting import figure,output_file,show
from bokeh.models import ColumnDataSource,CheckboxGroup,CustomJS,HoverTool,Range1d,RadioButtonGroup
from bokeh.layouts import row,column
from bokeh.transform import dodge
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
                   width = 800,
                   height = 800,
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
        
        #return check_boxes,p
        show(row(check_boxes,p))

    def get_genres(self,genres_series:pd.Series) -> pd.Series:
        """Converts string of genres for each song into a list"""
        final = []
        for song,genres in genres_series.items():
            #Removes surrounding square brackets and splits words into a list
            genres = genres.strip("[]")
            genres_list = genres.split(",")
            out = []
            for item in genres_list:
                #Removes trailing spaces and other outer values
                out.append(item.strip(" ''"))
            
            #Addes list and song id into a list
            final.append(tuple([song,out]))
        
        #put values into a final series
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

    def get_avg_playlist(self,column:str) -> pd.Series:
        """Gets the average of a song value grouped by playlist"""
        avg = pd.concat([self.songs.column[column],self.songs.column["PlaylistID"]],axis=1)
        return avg.groupby("PlaylistID").mean()

    def avg_bar(self):
        """Plots the bar chart comparing average song values to playlists and genres"""
        #Collects data
        avg_dance = self.get_avg_playlist("Dance")
        avg_energy = self.get_avg_playlist("Energy")
        avg_genre = self.avg_genre()
        playlist_name = self.playlists.column["Name"]
        data = pd.concat([avg_dance,avg_energy,avg_genre,playlist_name],axis=1)
        source = ColumnDataSource(data)

        energy = ColumnDataSource(data.sort_values("Energy",ascending=False))
        dance = ColumnDataSource(data.sort_values("Dance",ascending=False))


        #Generates figure
        p = figure(y_range = Range1d(0,1),title="Playlist average Dance scores",x_range=dance.data["Name"],width=1000,height=400,background_fill_color=self.black)
        p.xaxis.major_label_orientation = "vertical"
        p.grid.grid_line_color = None

        
        p2 = figure(y_range = Range1d(0,1),title="Playlist average Energy scores",x_range=energy.data["Name"],width=1000,height=400,background_fill_color=self.black)
        p2.xaxis.major_label_orientation = "vertical"
        p2.grid.grid_line_color = None

        #Generates both bars
        p.vbar(x="Name",top="Dance",source=dance,legend_label="Dance",width=0.8,color=self.green)
        p2.vbar(x="Name",top="Energy",source=energy,legend_label="Energy",width=0.8,color=self.white)

        show(column(p,p2))

    def playlist_size(self):
        """Will generate a pie chart showing the sizes of each playlist compared to others in the profile"""
        playlist_name = self.playlists.column["Name"]
        playlist_length = self.playlists.column["Length"]

        data = pd.concat([playlist_name,playlist_length],axis=1)
        print(data)


    def render(self):
        #self.dance_energy()
        #self.avg_bar()
        self.playlist_size()

        