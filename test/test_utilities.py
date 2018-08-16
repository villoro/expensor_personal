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


    def test_get_filename(self):
        """ Check that is able to connect to drobpox """

        name = u.io.get_money_lover_filename()

        self.assertIn(name.split(".")[-1], ["xls", "xlsx"])


    def test_get_df_trans(self):
        """ Test that is able to retrive a valid excel for transactions """

        dbx = u.io.get_dropbox_conector()
        df = u.io.get_df_transactions(dbx)

        # Check that all needed columns are present
        self.assertTrue(all([x in df.columns for x in c.cols.REPLACES_DF_TRANS]))


    def test_get_data_without_trans(self):
        """ Test that is able to retrive dataframes from data.xlsx """

        dbx = u.io.get_dropbox_conector()
        dfs = u.io.get_data_without_transactions(dbx)

        # Check that all needed dataframes are present
        self.assertTrue(all([x in dfs for x in c.dfs.ALL_FROM_DATA]))


    def test_get_data_from_loader(self):
        """ Test that is able to retrive all dataframes """

        dload = u.io.DataLoader()
        dload.sync()

        # Check that all needed dataframes are present
        self.assertTrue(all([x in dload.get_data() for x in c.dfs.ALL]))



    # ------------------------------ dfs -----------------------------------------------------------
    def test_fix_df_trans(self):
        """ Test that is able to retrive dataframes from data.xlsx """

        dbx = u.io.get_dropbox_conector()
        df = u.io.get_df_transactions(dbx)
        df = u.dfs.fix_df_trans(df)

        # Check that all needed columns are present
        self.assertTrue(all([x in df.columns for x in c.cols.DF_TRANS]))

        # Check that expenses and income are positive
        for x in [c.names.EXPENSES, c.names.INCOMES]:
            self.assertTrue(df[df[c.cols.TYPE] == x][c.cols.AMOUNT].min() > 0)


    def test_filter_data(self):
        """ Test that is able to filter by some column """

        dbx = u.io.get_dropbox_conector()
        df = u.io.get_df_transactions(dbx)
        df = u.dfs.fix_df_trans(df)

        # No filter no modifications
        self.assertEqual(df.shape, u.dfs.filter_data(df).shape)

        # Check that is able to filter using some personal categories
        aux = u.dfs.filter_data(df, "Menjar")[c.cols.CATEGORY].unique().tolist()
        self.assertEqual(aux, ["Menjar"])

        aux = u.dfs.filter_data(df, ["Transport", "Menjar"])[c.cols.CATEGORY].unique().tolist()
        self.assertEqual(sorted(aux), sorted(["Transport", "Menjar"]))


    def test_groupby(self):
        """ Test that is able group by timewindow """

        dbx = u.io.get_dropbox_conector()
        df = u.io.get_df_transactions(dbx)
        df = u.dfs.fix_df_trans(df)

        # When filtered by month, all dates are from day 1
        aux = u.dfs.group_df_by(df, "M")
        self.assertEqual(aux.index.strftime("%d").tolist(), ['01']*aux.shape[0])

        # When filtered by year index are ints
        aux = u.dfs.group_df_by(df, "Y")
        self.assertEqual(aux.index.min(), df[c.cols.YEAR].min())
        self.assertEqual(aux.index.max(), df[c.cols.YEAR].max())



if __name__ == '__main__':
    unittest.main()
