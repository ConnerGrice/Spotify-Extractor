from typing import Any, List
import sqlite3
from abc import ABC, abstractmethod

class Table(ABC):
    def __init__(self,database: sqlite3.Connection):
        self.database = database
        self.cursor = database.cursor()
        self.NAME = ""

    def sql_command_single(self,command:str,input:Any=()) -> None:
        try:
            self.cursor.execute(command,input)
        except Exception as e:
            self.database.rollback()
            raise e

    def sql_command_many(self,command:str,inputs:List) -> None:
        try:
            self.cursor.executemany(command,input)
        except Exception as e:
            self.database.rollback()
            raise e

    def check_exists(self) -> bool:
        """
        Checks if the table already exists
        """
        
        #Gets a the name of the table
        check_exists = f"""
        SELECT name FROM sqlite_master WHERE type='table' AND name='{self.NAME}'"""

        self.sql_command_single(check_exists)
        print(self.NAME)

        #Checks if the table exists
        if self.cursor.fetchone() == None:
            return False
        return True


    @abstractmethod
    def create_table(self) -> None:
        pass

    @abstractmethod
    def populate_table(self,data):
        pass


class Playlists(Table):
    def __init__(self,database):
        super().__init__(database)
        self.NAME = "Playlists"

        # if not self.check_exists():
        #     self.create_table()
        #     print("Creating Playlists")

    def create_table(self) -> None:
        create = """
        CREATE TABLE IF NOT EXISTS "Playlists"(
            PlaylistID int NOT NULL,
            Name char(255) NOT NULL,
            Owner char(255) NOT NULL,
            Length int NOT NULL,
            Version int NOT NULL,
            PRIMARY KEY (PlaylistID));
        """

        self.sql_command_single(create)


    def populate_table(self,data) -> None:
        print("populate table")







