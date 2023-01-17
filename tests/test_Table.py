import unittest
from classes.Tables import Playlists,Artists
from dataclasses import astuple
from classes import Items

class TestTable(unittest.TestCase):

    def test_populate_tuple(self):
        playlist = Playlists("Test.db")
        data = ("id","Testing","Conner",30,"version")
        playlist.populate_table(data)

        select = "SELECT * FROM Playlists"
        playlist.sql_command_single(select)
        result = playlist.cursor.fetchone()
        self.assertEqual(result,data)

    def test_populate_list(self):
        playlist = Playlists("Test.db")
        data = ["id","Testing","Conner",30,"version"]
        playlist.populate_table(data)

        select = "SELECT * FROM Playlists"
        playlist.sql_command_single(select)
        result = list(playlist.cursor.fetchone())
        self.assertEqual(result,data)
    
    def test_populate_attributes(self):
        playlist = Playlists("Test.db")
        data = astuple(Items.PlaylistItem("id","Testing","Conner",30,"version"))
        playlist.populate_table(data)

        select = "SELECT * FROM Playlists"
        playlist.sql_command_single(select)
        result = playlist.cursor.fetchone()
        self.assertEqual(result,data)

    def test_delete(self):
        artists = Artists("Test.db")
        data = ("id","Conner","Funk")
        artists.populate_table(data)
        artists.delete_rows()

        select = "SELECT * FROM Artists"
        artists.sql_command_single(select)
        self.assertIsNone(artists.cursor.fetchone())


    
    def test_name(self):
        playlist = Playlists("Test.db")
        self.assertEqual(playlist.NAME,"Playlists","Should be named Playlist")

    def test_exists(self):
        playlist = Playlists("Test.db")
        self.assertTrue(playlist.check_exists(),"Should exist")
    
    


if __name__ == "__main__":
    unittest.main()