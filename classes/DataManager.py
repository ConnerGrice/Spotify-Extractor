from dataclasses import dataclass,field
from typing import Any
from abc import abstractmethod
import pandas as pd

@dataclass
class DataManager:
    """Represents all the data from a given table"""
    df : pd.DataFrame
    id : pd.Series = field(init=False)
    column : dict[str:pd.Series] = field(init=False)
    
    def __post_init__(self) -> None:
        """Creates a dict of all the columns and thier corresponding values when the object is initialised"""
        self.column = {name:series for (name,series) in self.df.items()}
        self.id = pd.Series(self.df.index)

    def join_with(self,other_column:pd.Series,base_column:str) -> pd.DataFrame:
        """Combines 2 different columns from different tables together"""
        #Songs playlistID playlist Name
        combined =  pd.merge(self.column[base_column],other_column,right_index=True,left_on=base_column)
        return combined

    def map_of(self,other_column:pd.Series,base_column:str) -> dict[Any:Any]:
        """Creates a dictionary between a foreign key and another attribute"""
        joined = self.join_with(other_column,base_column)
        return {first:second for (first,second) in joined.itertuples(index=False)}
