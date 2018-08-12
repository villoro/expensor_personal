"""
    Utilities for pandas dataframes
"""

import pandas as pd

import constants as c


def group_df_by(df, timewindow):
    """
        Groups a dataframe by the given timewindow

        Args:
            df:         dataframe to group
            timewindow: temporal agrupation to use

        Returns:
            dataframe grouped
    """

    col = {"D": c.cols.DATE, "M": c.cols.MONTH_DATE, "Y": c.cols.YEAR}[timewindow]

    return df[[col, c.cols.AMOUNT]].groupby(col).sum()


def filter_data(df_input, values=None, col_name=c.cols.CATEGORY):
    """
        Filters the dataframe that will be reused in all plots

        Args:
            values:     values to include
            col_name:   reference column for filtering
    """

    df = df_input.copy()

    if values:
        if isinstance(values, list):
            df = df[df[col_name].isin(values)]
        else:
            df = df[df[col_name] == values]

    return df


def fix_df_trans(df_in):
    """
        It does all required transformations in order to use the transaction dataframe

        Args:
            df_in:  raw dataframe with transactions
    """

    df = df_in.rename(c.cols.REPLACES, axis="columns").copy()
    df = df[~df[c.cols.CATEGORY].isin(c.io.FORBIDDEN_CATEGORIES)]

    # Add time filter columns (store everything as string to ensure JSON compatibility)
    df[c.cols.DATE] = pd.to_datetime(df[c.cols.DATE])
    df[c.cols.MONTH_DATE] = pd.to_datetime(df[c.cols.DATE].dt.strftime("%Y-%m-01"))
    df[c.cols.MONTH] = df[c.cols.DATE].dt.month
    df[c.cols.YEAR] = df[c.cols.DATE].dt.year

    # Tag expenses/incomes
    df.loc[df[c.cols.AMOUNT] > 0, c.cols.TYPE] = c.names.INCOMES
    df[c.cols.TYPE].fillna(c.names.EXPENSES, inplace=True)

    # Amount as positve number
    df[c.cols.AMOUNT] = df[c.cols.AMOUNT].apply(abs)

    return df[c.cols.DF_TRANS]
