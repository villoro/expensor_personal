"""
    Tests for utilities.py
"""

import unittest

from src import constants as c
from src import utilities as u
from src.data_loader import DFS

class TestUtilities(unittest.TestCase):
    """Test utilities"""

    # ------------------------------ dfs -----------------------------------------------------------
    def test_fix_df_trans(self):
        """ Test that is able to retrive dataframes from data.xlsx """

        df = DFS[c.dfs.TRANS]

        # Check that all needed columns are present
        self.assertTrue(all([x in df.columns for x in c.cols.DF_TRANS]))

        # Check that expenses and income are positive
        for x in [c.names.EXPENSES, c.names.INCOMES]:
            self.assertTrue(df[df[c.cols.TYPE] == x][c.cols.AMOUNT].min() > 0)


    def test_filter_data(self):
        """ Test that is able to filter by some column """

        df = DFS[c.dfs.TRANS]

        # No filter no modifications
        self.assertEqual(df.shape, u.dfs.filter_data(df).shape)

        # Check that is able to filter using some personal categories
        aux = u.dfs.filter_data(df, "Menjar")[c.cols.CATEGORY].unique().tolist()
        self.assertEqual(aux, ["Menjar"])

        aux = u.dfs.filter_data(df, ["Transport", "Menjar"])[c.cols.CATEGORY].unique().tolist()
        self.assertEqual(sorted(aux), sorted(["Transport", "Menjar"]))


    def test_groupby(self):
        """ Test that is able group by timewindow """

        df = DFS[c.dfs.TRANS]

        # When filtered by month, all dates are from day 1
        aux = u.dfs.group_df_by(df, "M")
        self.assertEqual(aux.index.strftime("%d").tolist(), ['01']*aux.shape[0])

        # When filtered by year index are ints
        aux = u.dfs.group_df_by(df, "Y")
        self.assertEqual(aux.index.min(), df[c.cols.YEAR].min())
        self.assertEqual(aux.index.max(), df[c.cols.YEAR].max())



if __name__ == '__main__':
    unittest.main()
