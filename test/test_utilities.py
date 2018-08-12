"""
    Tests for utilities.py
"""

import unittest

from src import constants as c
from src import utilities as u

class TestUtilities(unittest.TestCase):
    """Test utilities"""

    dummy_path = "imaginary_path_for_testing/"

    # ------------------------------ palette -------------------------------------------------------
    def test_palette(self):
        """
            Test palette
        """

        # Test that you can call one color with a list of tuples or with a tuple
        self.assertEqual(u.get_colors([("red", 100)]), "#FFCDD2")
        self.assertEqual(u.get_colors(("red", 100)), "#FFCDD2")

        # Test that you can call more than one color
        self.assertEqual(u.get_colors([("red", 100), ("blue", 100)]),
                         ["#FFCDD2", "#BBDEFB"])


    # ------------------------------ io ------------------------------------------------------------
    def test_dropbox_connector(self):
        """ Check that is able to connect to drobpox """

        self.assertIsNotNone(u.io.get_dropbox_conector())


    def test_get_df_trans(self):
        """ Test that is able to retrive a valid excel for transactions """

        dbx = u.io.get_dropbox_conector()

        df = u.io.get_df_transactions(dbx)

        # Check that all needed columns are present
        self.assertTrue(all([x in df.columns for x in c.cols.REPLACES_DF_TRANS]))


    def test_get_data_without_transactions(self):
        """ Test that is able to retrive dataframes from data.xlsx """

        dbx = u.io.get_dropbox_conector()

        dfs = u.io.get_data_without_transactions(dbx)

        # Check that all needed dataframes are present
        self.assertTrue(all([x in dfs for x in c.dfs.ALL_FROM_DATA]))



if __name__ == '__main__':
    unittest.main()
