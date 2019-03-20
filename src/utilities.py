"""
    Utilities for pandas dataframes
"""

import pandas as pd
from v_palette import get_colors

import constants as c


def fix_df_trans(df_in):
    """
        It does all required transformations in order to use the transaction dataframe

        Args:
            df_in:  raw dataframe with transactions
    """

    df = df_in.rename(c.cols.REPLACES_DF_TRANS, axis="columns").copy()
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


def get_ebit(df_in):
    """
        Changes the sign of expenses in order to calc EBIT
    """
    df = df_in.copy()
    mfilter = df[c.cols.TYPE] == c.names.EXPENSES
    df.loc[mfilter, c.cols.AMOUNT] = -df.loc[mfilter, c.cols.AMOUNT]

    return df


def group_df_by(df_in, timewindow, dfg=None):
    """
        Groups a dataframe by the given timewindow

        Args:
            df:         dataframe to group
            timewindow: temporal agrupation to use
            dfg:        dataframe that will be used to check all unique time values

        Returns:
            dataframe grouped
    """

    if timewindow is None:
        return df_in

    col = {"D": c.cols.DATE, "M": c.cols.MONTH_DATE, "Y": c.cols.YEAR}[timewindow]

    # Group by date
    df = df_in.copy()[[col, c.cols.AMOUNT]].groupby(col).sum()

    if dfg is None:
        return df

    # Fill missing rows based on unique values of input data
    return df.reindex(dfg[col].unique(), fill_value=0)


def time_average(df_in, months, exponential=False):
    """ do some time average """

    # No negative values
    months = max(0, months)

    # Exponential moving average
    if exponential:
        df = df_in.ewm(span=months, min_periods=0, adjust=False, ignore_na=False)

    # Regular moving average
    else:
        df = df_in.rolling(months, min_periods=1)

    return df.mean().apply(lambda x: round(x, 2))


def group_df_with_time_avg(df_in, timewindow, months, dfg=None):
    """ groups a dataframe by a timewindow and then do some time average """

    return time_average(group_df_by(df_in, timewindow, dfg), months)


def normalize_index(df1, df2):
    """ Force two dataframes to have the same indexs """

    index = df2.index if df2.shape[0] > df1.shape[0] else df1.index
    df1 = df1.reindex(index).fillna(0)
    df2 = df2.reindex(index).fillna(0)

    return df1, df2
