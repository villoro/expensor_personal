"""
    Tests for utilities.py
"""

import unittest

from src import constants as c
from src import data_loader as dload

class TestDataLoader(unittest.TestCase):
    """Test utilities"""

    # ------------------------------ io ------------------------------------------------------------
    def test_dropbox_connector(self):
        """ Check that is able to connect to drobpox """

        self.assertIsNotNone(dload.DBX)


    def test_get_filename(self):
        """ Check that is able to connect to drobpox """

        name = dload.get_money_lover_filename()

        self.assertIn(name.split(".")[-1], ["xls", "xlsx"])


    def test_get_df_trans(self):
        """ Test that is able to retrive a valid excel for transactions """

        df = dload.get_df_transactions()

        # Check that all needed columns are present
        self.assertTrue(all([x in df.columns for x in c.cols.REPLACES_DF_TRANS.values()]))


    def test_get_data_without_trans(self):
        """ Test that is able to retrive dataframes from data.xlsx """

        dfs = dload.get_data_without_transactions()

        # Check that all needed dataframes are present
        self.assertTrue(all([x in dfs for x in c.dfs.ALL_FROM_DATA]))


    def test_get_data_from_loader(self):
        """ Test that is able to retrive all dataframes """

        # Check that all needed dataframes are present
        self.assertTrue(all([x in dload.DFS for x in c.dfs.ALL]))



if __name__ == '__main__':
    unittest.main()
