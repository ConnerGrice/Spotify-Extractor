import unittest
from dataclasses import astuple
from classes import SpotifyAPI
from classes import Items

class TestSpotifyAPI(unittest.TestCase):
    def test_remove_artist(self):
        
        api = SpotifyAPI.SpotifyAPI()

        track1 = Items.TrackItem(
            "id",
            "testing",
            123,
            1.0,
            1.0,
            1.0,
            "art_id",
            "album_id",
            "playlist_id")
        track2 = Items.TrackItem(
            "id",
            "testing",
            123,
            1.0,
            1.0,
            1.0,
            "art_id",
            "album_id",
            "playlist_id")
        track3 = Items.TrackItem(
            "id",
            "testing",
            123,
            1.0,
            1.0,
            1.0,
            "art_id_different",
            "album_id",
            "playlist_id")

        result = api.remove_dup_artists([track1,track2,track3])
        self.assertEqual(len(result),2)

    def test_remove_albums(self):
        
        api = SpotifyAPI.SpotifyAPI()

        track1 = Items.TrackItem(
            "id",
            "testing",
            123,
            1.0,
            1.0,
            1.0,
            "art_id",
            "album_id_diff",
            "playlist_id")
        track2 = Items.TrackItem(
            "id",
            "testing",
            123,
            1.0,
            1.0,
            1.0,
            "art_id",
            "album_id_diffagain",
            "playlist_id")
        track3 = Items.TrackItem(
            "id",
            "testing",
            123,
            1.0,
            1.0,
            1.0,
            "art_id_different",
            "album_id",
            "playlist_id")

        result = api.remove_dup_albums([track1, track2, track3])
        self.assertEqual(len(result),3)
    
    def test_get_single_playlist(self):
        """Tests the get_single_playlist method"""
        api = SpotifyAPI.SpotifyAPI()

        playlist_id = "5dSHjPEsWIAZhq9HrF5XHO"

        results = api.get_single_playlist(playlist_id=playlist_id)

        results = astuple(results)
        expected = ("5dSHjPEsWIAZhq9HrF5XHO","Bhonk","connergrice",24,"MjUsMTA4YjMwYWE4ODU1MTI4ZGE5OGUwOWYxMTYzMThlODMxZDY3YjljYg==")
        self.assertEqual(expected, results)

if __name__ == "__main__":
    unittest.main()