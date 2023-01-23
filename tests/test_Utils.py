import unittest
from pandas.util.testing import assert_frame_equal
import pandas as pd
import numpy as np
from classes import Utils

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
if __name__ == '__main__':
    unittest.main()