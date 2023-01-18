import unittest
import pandas as pd

from classes.Tables import Playlists,Songs,Albums,Artists
from classes.Items import ArtistItem
from classes.Database import Database

class TestDatabase(unittest.TestCase):

    """Tests the databases ability to fetch the titles of all tables"""
    def test_table_outputs(self):
        pl = Playlists("tests/Test.db")
        s = Songs("tests/Test.db")        
        al = Albums("tests/Test.db")        
        ar = Artists("tests/Test.db")

        for table in [pl,s,al,ar]:
            table.close_table()

        db = Database("tests/Test.db")
        results = db.get_tables()
        db.close_table()

        self.assertEqual(results,['Songs','Artists','Playlists','Albums'])

    def test_get_colmuns(self):
        """Tests the databases ability to get the colmun names"""
        db = Database("tests/Test.db")

        results = db.get_columns("Artists")
        db.close_table()
        self.assertEqual(results,["ArtistID","Name","Genre"])

    def test_table_info(self):
        """Tests if the database can collect the correct information"""
        expected = {'Artists':['ArtistID','Name','Genre']}

        db = Database("tests/Test.db")
        results = db.table_info
        db.close_table()

        self.assertEqual(results['Artists'],expected['Artists'])

    def test_select_from(self):
        """Tests if select_from outputs the correct dataframe"""
        artists = Artists("tests/Test.db")
        artists.delete_rows()
        artists.populate_table([("123","Conner","Funk"),("124","Conner2","Funk")])
        artists.close_table()

        db = Database("tests/Test.db")

        table = "Artists"
        columns = ["Name","Genre"]

        result = db.select_from(table,columns)

        expected = [("123","Conner","Funk"),("124","Conner2","Funk")]

        self.assertEqual(result, expected)

    def test_select_single(self):
        artists = Artists("tests/Test.db")
        artists.delete_rows()
        artists.populate_table([("123","Conner","Funk"),("124","Conner2","Funk")])
        artists.close_table()

        db = Database("tests/Test.db")

        result = db.select_single_id("Artists","123")
        self.assertEqual(result,["123","Conner","Funk"])

    def test_insert(self):
        artists = Artists("tests/Test.db")
        artists.delete_rows()
        artists.populate_table([("123","Conner","Funk"),("124","Conner2","Funk")])
        artists.close_table()

        db = Database("tests/Test.db")

        new = ArtistItem("1235","ConnerAgain","Rock")
        db.insert("Artists",new)

        data = db.select_from("Artists",["Name","Genre"])
        expected = [("123","Conner","Funk"),("124","Conner2","Funk"),("1235","ConnerAgain","Rock")]

        self.assertEqual(data,expected)

    def test_replace(self):
        artists = Artists("tests/Test.db")
        artists.delete_rows()
        artists.populate_table([("123","Conner","Funk"),("124","Conner2","Funk")])
        artists.close_table()

        db = Database("tests/Test.db")

        new = ArtistItem("123","ConnerAgain","Rock")
        db.insert("Artists",new)

        data = db.select_from("Artists",["Name","Genre"])
        expected = [("124","Conner2","Funk"),("123","ConnerAgain","Rock")]

        self.assertEqual(data,expected)

if __name__ == '__main__':
    unittest.main()