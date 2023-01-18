import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from classes.Tables import Playlists,Songs,Albums,Artists
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

        expected = pd.DataFrame([["Conner","Funk"],["Conner2","Funk"]],columns=columns,index=["123","124"])

        assert_frame_equal(result, expected)




if __name__ == '__main__':
    unittest.main()