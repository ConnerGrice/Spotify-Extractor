import unittest
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

        expected = {'Artists':['ArtistID','Name','Genre']}

        db = Database("tests/Test.db")
        results = db.table_info
        db.close_table()

        self.assertEqual(results['Artists'],expected['Artists'])




if __name__ == '__main__':
    unittest.main()