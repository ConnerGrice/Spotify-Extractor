import unittest
from classes.Tables import Table,Playlists,Artists,Songs
from dataclasses import astuple
from classes import Items
import sqlite3

class TestTable(unittest.TestCase):

    def test_populate_tuple(self):
        """Tests that data can be input"""
        playlist = Playlists("tests/Test.db")
        playlist.delete_rows()
        data = [("id","Testing","Conner",30,"version")]
        playlist.populate_table(data)

        select = "SELECT * FROM Playlists"
        playlist.sql_command_single(select)
        result = playlist.cursor.fetchone()
        self.assertEqual([result],data)
    
    def test_populate_attributes(self):
        """Tests that item objects can be passed as data"""
        playlist = Playlists("tests/Test.db")
        playlist.delete_rows()
        data = [astuple(Items.PlaylistItem("id","Testing","Conner",30,"version"))]
        playlist.populate_table(data)

        select = "SELECT * FROM Playlists"
        playlist.sql_command_single(select)
        result = playlist.cursor.fetchone()
        self.assertEqual([result],data)

    def test_delete(self):
        """Tests if rows can be deleted"""
        artists = Artists("tests/Test.db")
        artists.delete_rows()
        data = [("id","Conner","Funk")]
        artists.populate_table(data)
        artists.delete_rows()

        select = "SELECT * FROM Artists"
        artists.sql_command_single(select)
        self.assertIsNone(artists.cursor.fetchone())

    def test_name(self):
        """Tests that names get carried between Table objects"""
        playlist = Playlists("tests/Test.db")
        self.assertEqual(playlist.NAME,"Playlists","Should be named Playlist")

    def test_exists(self):
        """Checks the method that checks if a tabel exists"""
        playlist = Playlists("tests/Test.db")
        self.assertTrue(playlist.check_exists(),"Should exist")    

    def test_track_comp_keys(self):
        """Tests if compund primary keys works"""
        tracks = Songs("tests/Test.db")
        tracks.delete_rows()
        track1 = Items.TrackItem("id","Track1",23,1.0,1.0,1.0,"art_id","alb_id","play_id")
        track2 = Items.TrackItem("id","Track1",23,1.0,1.0,1.0,"art_id","alb_id","play_id_diff")
        data = [astuple(track1),astuple(track2)]

        try:
            tracks.populate_table(data)
        except sqlite3.IntegrityError as e:
            self.fail(e)

    def test_track_ignore(self):
        """Tests if compund primary keys works"""
        tracks = Songs("tests/Test.db")
        tracks.delete_rows()
        track1 = Items.TrackItem("id","Track1",23,1.0,1.0,1.0,"art_id","alb_id","play_id")
        track2 = Items.TrackItem("id","Track1",23,1.0,1.0,1.0,"art_id","alb_id","play_id_diff")
        track3 = Items.TrackItem("id","Track1",23,1.0,1.0,1.0,"art_id","alb_id","play_id_diff")
        data = [astuple(track1),astuple(track2),astuple(track3)]

        try:
            tracks.populate_table(data)
        except sqlite3.IntegrityError as e:
            self.fail(e)

        tracks.sql_command_single("SELECT * FROM Songs")
        self.assertEqual(len(tracks.cursor.fetchall()),2)

if __name__ == "__main__":
    unittest.main()