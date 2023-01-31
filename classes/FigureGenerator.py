from classes.DataManager import DataManager
from bokeh.plotting import figure,output_file,show
from bokeh.models import ColumnDataSource,CDSView,BooleanFilter,GroupFilter,CheckboxGroup,CustomJS
from bokeh.layouts import row
import pandas as pd

class EventHandler:
    def dance_energy_handler(attr,old,new):
        print("test",new)
        print("test",old)

class FigureGenerator:
    def __init__(self,songs:DataManager,playlists:DataManager,albums:DataManager,artists:DataManager) -> None:
        self.songs = songs
        self.playlists = playlists
        self.albums = albums
        self.artists = artists

        self.handler = EventHandler()

        output_file("output.html")

    def dance_energy_handler(attr,old,new):
        print("test",new)
        print("test",old)

    def dance_energy(self):
        dance = self.songs.column["Dance"]
        energy = self.songs.column["Energy"]

        names = self.songs.column["PlaylistID"]
        names = names.map(self.songs.map_of(self.playlists.column["Name"],"PlaylistID"))
        data = pd.concat([dance,energy,names],axis=1)
        
        labels = list(data.PlaylistID.unique())
        data["PlaylistID"] = data["PlaylistID"].map({name:label for (name,label) in zip(labels,range(len(labels)))})
        source = ColumnDataSource(data)

        p = figure(title= "Dance vs Energy",x_axis_label="Dance",y_axis_label="Energy")
        p.scatter(x="Dance",y="Energy",source=source)

        check_boxes = CheckboxGroup(labels=labels,active=list(range(len(labels))))

        callback = CustomJS(args=dict(source=source),code="""
            var data = source.data;
            var new_index = [];
            var new_dance = [];
            var new_energy = [];
            var new_label = [];

            const active = cb_obj.active;
            
            var index = data['index'];
            var dance = data['Dance'];
            var energy = data['Energy'];
            var labels = data['PlaylistID'];

            for (let i=0;i<dance.length;i++){
                for (let j=0;j<active.length;j++){
                    if (labels[i] == active[j]){
                        console.log(labels[i])
                        new_index.push(index[i]);
                        new_dance.push(dance[i]);
                        new_energy.push(energy[i]);
                        new_label.push(labels[i])
                    }
                }
            }   

            data['Dance'] = new_dance;
            data['Energy'] = new_energy;
            data['PlaylistID'] = new_label;
            data['index'] = new_index

            source.change.emit();
        """)

        check_boxes.js_on_change("active",callback)

        
        show(row(check_boxes,p))

        