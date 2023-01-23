import unittest
from pandas.util.testing import assert_frame_equal
import pandas as pd
import numpy as np
from classes import Utils
from classes.Database import Database
from classes.Tables import Songs,Playlists

class TestUtils(unittest.TestCase):
    ...
    def test_comparison(self):
        """Testing the comparison function"""
        new_series = pd.Series([1, 2, 3],index = [1,2,3])
        old_series = pd.Series([1, 2],index = [1,2])

        difference = Utils.comparison(old_series,new_series)

        result = pd.DataFrame([[np.nan,3]],index = [3],columns=["old", "new"])

        assert_frame_equal(difference, result)

    def test_added(self):
        """Testing the been_added function"""
        new_series = pd.Series([1, 2, 3],index = [1,2,3])
        old_series = pd.Series([1, 2],index = [1,2])

        difference = Utils.comparison(old_series,new_series)

        self.assertTrue(Utils.been_added(difference.values[0]))

    def test_removed(self):
        """Testing the been_removed function"""
        old_series = pd.Series([1, 2, 3],index = [1,2,3])
        new_series = pd.Series([1, 2],index = [1,2])

        difference = Utils.comparison(old_series,new_series)

        self.assertTrue(Utils.been_removed(difference.values[0]))

    def test_collect_from_ids(self):
        """Tests the function that generates a list of ids using another tables primary key"""
        songs = Songs("tests/Test.db")
        songs.delete_rows()

        data = [
            ("1","Song1",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
            ("2","Song2",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
            ("3","Song3",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
            ("4","Song4",12,1.0,1.0,1.0,"artistID1","albumID1","playlist2"),
            ("5","Song5",12,1.0,1.0,1.0,"artistID1","albumID1","playlist3"),
            ("6","Song6",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
        ]

        songs.populate_table(data)

        songs.close_table()

        playlists = Playlists("tests/Test.db")
        playlists.close_table()

        db = Database("tests/Test.db")

        result = Utils.collect_from_ids(db,"Songs","Playlists",'"playlist1"')
        expected = ["1","2","3","6"]
        self.assertEqual(result, expected)

    def test_get_everything(self):
        songs = Songs("tests/Test.db")
        songs.delete_rows()

        data = [
            ("1","Song1",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
            ("2","Song2",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
            ("3","Song3",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
            ("4","Song4",12,1.0,1.0,1.0,"artistID1","albumID1","playlist2"),
            ("5","Song5",12,1.0,1.0,1.0,"artistID1","albumID1","playlist3"),
            ("6","Song6",12,1.0,1.0,1.0,"artistID1","albumID1","playlist1"),
        ]

        songs.populate_table(data)

        songs.close_table()

        db = Database("tests/Test.db")

        result = Utils.get_everything_id(db,"Songs")
        expected = ["1","2","3","4","5","6"]
        self.assertEqual(result,expected)      

if __name__ == '__main__':
    unittest.main()