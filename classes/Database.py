import sqlite3
import pandas as pd
from typing import Any,Iterable
from itertools import chain

class Database:
    def __init__(self,db_name:str) -> None:
        self.database = sqlite3.connect(db_name)
        self.cursor = self.database.cursor()

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

        data = self.sql_command_single(command)

        columns = self.cursor.fetchall()
        items = list(chain(*columns))
        return items
    
    def collect_table_info(self) -> dict[str,list[str]]:
        output = {}
        tables = self.get_tables()
        for table in tables:
            columns = self.get_columns(table)
            output[table] = columns
        
        return output



