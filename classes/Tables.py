from typing import Any, Iterable, List
import sqlite3
from abc import ABC, abstractmethod

class Table(ABC):
    """Base class for specific tables objects"""
    def __init__(self,db_name:str) -> None:
        self.database = sqlite3.connect(db_name)
        self.cursor = self.database.cursor()

    def sql_command_single(self,command:str,inputs:Any=()) -> None:
        """Executes command with only one argument"""
        try:
            self.cursor.execute(command,inputs)
        except Exception as e:
            self.database.rollback()
            raise e

    def sql_command_many(self,command:str,inputs:Iterable) -> None:
        """Executes command with many arguments"""
        try:
            self.cursor.executemany(command,inputs)
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

    def delete_rows(self) -> None:
        command = f"""
        DELETE FROM {self.NAME}"""

        self.sql_command_single(command)

    @abstractmethod
    def create_table(self) -> None:
        pass

    @abstractmethod
    def populate_table(self,data):
        pass

class Playlists(Table):
    def __init__(self,db_name) -> None:
        super().__init__(db_name)
        self.NAME = "Playlists"

        if not self.check_exists():
            self.create_table()
            print("Creating Playlists")

    def create_table(self) -> None:
        """Creates a Playlists table"""

        create = f"""
        CREATE TABLE IF NOT EXISTS "{self.NAME}"(
            PlaylistID int NOT NULL,
            Name char(255) NOT NULL,
            Owner char(255) NOT NULL,
            Length int NOT NULL,
            Version int NOT NULL,
            PRIMARY KEY (PlaylistID));
        """

        self.sql_command_single(create)


    def populate_table(self,data:Iterable) -> None:
        """Populates the Playlists table"""
        
        command = f"""
        INSERT INTO {self.NAME} VALUES
        (?,?,?,?,?)"""

        self.sql_command_single(command,data)

        

class Artists(Table):
    def __init__(self,db_name) -> None:
        super().__init__(db_name)
        self.NAME = "Artists"

        #Creates table if it doesnt exist
        if not self.check_exists():
            self.create_table()
            print("Creating Playlists")
        

    def create_table(self) -> None:
        """Creates an Artist table"""

        create = F"""
        CREATE TABLE IF NOT EXISTS "{self.NAME}"(
            ArtistID int NOT NULL,
            Name char(255) NOT NULL,
            Genre char(255) NOT NULL,
            PRIMARY KEY (ArtistID)
        );"""

        self.sql_command_single(create)
    
    def populate_table(self,data:Iterable) -> None:
        """Populates the Artists table"""
        
        command = f"""
        INSERT INTO {self.NAME} VALUES
        (?,?,?)"""

        self.sql_command_single(command,data)

class Albums(Table):
    def __init__(self,db_name) -> None:
        super().__init__(db_name)
        self.NAME = "Albums"

        #Creates table if it doesn't exist
        if not self.check_exists():
            self.create_table()
            print("Creating Playlists")

    def create_table(self) -> None:
        """Creates an Albums table"""

        create = F"""
        CREATE TABLE IF NOT EXISTS "{self.NAME}"(
            AlbumID int NOT NULL,
            Name char(255) NOT NULL,
            ReleaseDate date NOT NULL,
            ArtistID int NOT NULL,
            PRIMARY KEY (AlbumID),
            FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
        );"""

        self.sql_command_single(create)
    

    def populate_table(self,data:Iterable) -> None:
        """Populates the Albums table"""
        
        command = f"""
        INSERT INTO {self.NAME} VALUES
        (?,?,?,?)"""

        self.sql_command_single(command,data)

class Songs(Table):
    def __init__(self,db_name) -> None:
        super().__init__(db_name)
        self.NAME = "Songs"
    
        #Creates table if it doesn't exist
        if not self.check_exists():
            self.create_table()
            print("Creating Playlists")

    def create_table(self) -> None:
        """Creates a Songs table"""

        create = f"""
        CREATE TABLE IF NOT EXISTS "{self.NAME}"(
            SongID int NOT NULL,
            Name char(255) NOT NULL,
            Duration int NOT NULL,
            Dance float NOT NULL,
            Tempo float NOT NULL,
            Energy float NOT NULL,
            ArtistID int NOT NULL,
            AlbumID int NOT NULL,
            PlaylistID int NOT NULL,
            PRIMARY KEY(SongID),
            FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID),
            FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID),
            FOREIGN KEY (PlaylistID) REFERENCES Playlists(PlaylistID)
        );"""

        self.sql_command_single(create)
    

    def populate_table(self,data:Iterable) -> None:
        """Populates the Songs table"""
        
        command = f"""
        INSERT INTO {self.NAME} VALUES
        (?,?,?,?,?,?,?,?,?)"""

        self.sql_command_single(command,data)





