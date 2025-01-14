import sqlite3
import pandas as pd
import numpy as np
from classes.Items import Item
from typing import Any,Iterable,List
from dataclasses import astuple
from itertools import chain

class Database:
    def __init__(self,db_name:str) -> None:
        self.database = sqlite3.connect(db_name)
        self.cursor = self.database.cursor()


        """
        table_info = {table1:[primary_key,header2,...],
                    table2:[primary_key,header2,...],
                    ...}"""
        self.table_info = self.collect_table_info()


    def sql_command_single(self,command:str,inputs:Any=()) -> None:
        """Executes command with only one argument"""
        try:
            self.cursor.execute(command,inputs)
            self.database.commit()
        except Exception as e:
            self.database.rollback()
            raise e

    def sql_command_many(self,command:str,inputs:Iterable) -> None:
        """Executes command with many arguments"""
        try:
            self.cursor.executemany(command,inputs)
            self.database.commit()
        except Exception as e:
            self.database.rollback()
            raise e

    def close_table(self) -> None:
        """Closes the sql connection"""
        self.database.close()

    def get_tables(self) -> list[str]:
        """Gets a list of the tables in the database"""
        
        #Gets the names of all tables in database
        command = """SELECT name FROM sqlite_master WHERE type='table'"""
        self.sql_command_single(command)

        #Gets those values as a list of tuples of strings
        # [(title1,),(title2,),...]
        tables = self.cursor.fetchall()

        #Converts the list of tuples into a list
        items = list(chain(*tables))
        return items

    def get_columns(self,table:str) -> list[str]:
        """Gets a list of the columns from a table"""

        command = f"""SELECT name FROM pragma_table_info('{table}') ORDER BY cid;"""

        self.sql_command_single(command)

        columns = self.cursor.fetchall()
        items = list(chain(*columns))
        return items
    
    def collect_table_info(self) -> dict[str,list[str]]:
        """Collects the table titles and column names from the database"""
        output = {}
        tables = self.get_tables()
        for table in tables:
            columns = self.get_columns(table)
            output[table] = columns
        
        return output

    def select_from(self,table:str,columns:list[str]) -> list[tuple[str]]:
        """Allows selection of columns of data"""
        id_column = self.table_info[table][0]

        command = f"SELECT {id_column}"

        if columns:
            for column in columns:
                command += f",{column}"

        command += f" FROM '{table}'"

        self.sql_command_single(command)

        data = self.cursor.fetchall()
        return data

    def select_all(self,table:str) -> pd.DataFrame:
        """Allows the user to select all columns from a table"""
        columns = self.table_info[table][1:]
        data = np.array(self.select_from(table,columns))
        df = pd.DataFrame(data[:,1:],index=data[:,0],columns=columns)
        df = df.apply(pd.to_numeric,errors="ignore")
        return df

    def select_with_contraint(self,table:str,values:list[str],constraint:str,constraint_value:str) -> list[tuple[str]]:
        """Allows for a selection with a specific constraint"""
        #Turns list of strings into a string of the correct format
        value_string = ""
        for value in values:
            value_string += value+","
        
        value_string = value_string.strip(",")

        command = f"SELECT {value_string} FROM {table} WHERE {constraint} = {constraint_value}"
        self.sql_command_single(command)
        data = self.cursor.fetchall()
        return data 

    def select_single_id(self,table:str,id:str) -> List:
        """Allows for the selection of a single entry using its primary key"""
        id_column = self.table_info[table][0]
        command = f"SELECT * FROM {table} WHERE {id_column} = '{id}'"

        self.sql_command_single(command)

        data = self.cursor.fetchall()
        data = list(chain(*data))
        return data

    def delete_with_contraint(self,table:str,constraint:str,data:list[tuple]) -> None:
        """Deletes entires to a table using a constraint"""
        command = f"DELETE FROM {table} WHERE {constraint} = ?"
        self.sql_command_many(command,data)

    def delete_with_contraint_and(self,table:str,constraint:list[str],data:list[tuple]) -> None:
        """Deletes entires to a table using multiple constrains and AND condition"""
        command = f"DELETE FROM {table} WHERE {constraint[0]} = ? AND {constraint[1]} = ?"
        self.sql_command_many(command,data)


    def insert_single(self,table:str,item:Item) -> None:
        """Allows for the insertion or replacement of an entry"""
        item_data = astuple(item)

        command = f"INSERT OR REPLACE INTO {table} VALUES {item_data}"
        self.sql_command_single(command)
    
    def insert_many(self,table:str,items:list[Item]) -> None:
        """Allows for the insertion or replacement of many entires"""
        data = [astuple(item) for item in items]
        command = f"INSERT OR REPLACE INTO {table} VALUES ("

        command += ",".join(["?"]*len(data[0])) + ")"

        self.sql_command_many(command,data)




