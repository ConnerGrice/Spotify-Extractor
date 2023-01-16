import unittest
from classes.Tables import Playlists

class TestTable(unittest.TestCase):

    def test_name(self):
        playlist = Playlists("Database.db")
        self.assertEqual(playlist.NAME,"Playlists","Should be named Playlist")

    def test_exists(self):
        playlist = Playlists("Database.db")
        self.assertTrue(playlist.check_exists(),"Should exist")

    


if __name__ == "__main__":
    unittest.main()