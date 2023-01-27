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
    items = db.select_from(table,None)
    items = list(chain(*items))
    return items