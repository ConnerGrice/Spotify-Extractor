import pandas as pd
import numpy as np

def comparison(old:pd.Series, new:pd.Series) -> pd.DataFrame:
    """Compares old and new list of playlists and finds the differences"""

    #Combines both series of playlists versions
    combined = pd.concat([old,new],axis=1,keys=["old","new"])
    
    #Gets all the differences between playlists
    diff = combined.loc[combined.old != combined.new]

    return diff

def what_change(diff:pd.DataFrame) -> bool:
    """Finds what kind of change was made to the playlists"""

    for item in diff.values:
        if been_added(item):
            print(item,"Added")
            return True
            #Insert into database
        elif been_removed(item):
            print(item,"Removed")
            return False
            #Delete from database
        else:
            print(item,"Modified")
            return True
            #Insert into database

def been_added(row) -> bool:
    """Determines whether a new playlist has been added"""
    return pd.isnull(row[0]) and not pd.isnull(row[1])

def been_removed(row) -> bool:
    """Determines whether a playlist has been removed"""
    return pd.isnull(row[1]) and not pd.isnull(row[0]) 



#6:Added
#2:Removed
old = pd.Series(['1','2','3','4','5'],index = [1,2,3,4,5],name="Test_old")
new = pd.Series(['1','3',"s",'5','6'],index = [1,3,4,5,6],name="Test_new")


#print(pd.notna(np.array(['d','e']).any()))
comparison(old, new)