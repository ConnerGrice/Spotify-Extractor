import unittest
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

if __name__ == "__main__":
    unittest.main()