import pandas as pd
import numpy as np
from itertools import chain
from classes.Database import Database


def comparison(old:pd.Series, new:pd.Series) -> pd.DataFrame:
    """Compares old and new list of playlists and finds the differences"""

    #Combines both series of playlists versions
    combined = pd.concat([old,new],axis=1,keys=["old","new"])
    
    #Gets all the differences between playlists
    diff = combined.loc[combined.old != combined.new]

    return diff

def what_change(diff:pd.DataFrame) -> list[bool]:
    """Finds what kind of change was made to the playlists
    True: Modified or added
    False: Removed"""
    outcomes = []

    for item in diff.values:
        if been_added(item):
            outcomes.append(True)
            #Insert into database
        elif been_removed(item):
            outcomes.append(False)
            #Delete from database
        else:
            outcomes.append(True)
            #Insert into database

    return outcomes
def been_added(row) -> bool:
    """Determines whether a new playlist has been added"""
    return pd.isnull(row[0]) and not pd.isnull(row[1])

def been_removed(row) -> bool:
    """Determines whether a playlist has been removed"""
    return pd.isnull(row[1]) and not pd.isnull(row[0]) 

def collect_from_ids(db:Database,child_table:str,parent_table:str,id:str) -> list[str]:
    """Collects all the items of a table based on a foreign key"""

    #Gets the column name for both tables
    child_id_col = db.table_info[child_table][0]
    parent_id_col = db.table_info[parent_table][0]

    #Gets the selected items 
    items = db.select_with_contraint(child_table,[child_id_col],parent_id_col,id)
    items = list(chain(*items))
    return items

def get_everything_id(db:Database,table:str) -> list[str]:
    """Gets a list of primary keys for all entries in a given table"""
    items = db.select_from(table,None)
    items = list(chain(*items))
    return items

def delete_songs(db:Database,playlist_id:str) -> None:
    """Deletes all the songs from a given playlist from the database"""
    removed_songs = collect_from_ids(db,"Songs","Playlists",f'"{playlist_id}"')
    removed_songs = [(s,playlist_id) for s in removed_songs]

    db.delete_with_contraint_and("Songs",["SongID","PlaylistID"],removed_songs)

def cascade_delete_from_songs(db:Database,table:str) -> None:
    """Removes all info from other tables if they are not connected to a song in the database"""
    #Gets id column from table
    table_id = db.table_info[table][0]

    #Gets ids of all items in the table
    before_ids = set(get_everything_id(db,table))

    #Gets ids of all items connected to remaining songs
    after_ids = set(np.array(db.select_from("Songs",[table_id]))[:,1])

    #Gets the items that are no longer connected to songs
    removed_ids = before_ids - after_ids
    removed_ids = [(a,) for a in removed_ids]

    #Delete from database
    db.delete_with_contraint(table,table_id,removed_ids)