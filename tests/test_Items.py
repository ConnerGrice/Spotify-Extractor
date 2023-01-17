import unittest
from classes import Items

class TestItem(unittest.TestCase):
    def test_eq_true(self):
        playlist1 = Items.PlaylistItem("id","testing_different","owner",34,"version")
        playlist2 = Items.PlaylistItem("id","testing","owner",34,"version")
        result = playlist1 == playlist2
        self.assertTrue(result)

    def test_eq_false(self):
        playlist1 = Items.PlaylistItem("id_different","testing","owner",50,"version")
        playlist2 = Items.PlaylistItem("id","testing","owner",34,"version")
        result = playlist1 == playlist2
        self.assertFalse(result)

        