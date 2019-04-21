"""
    Utilities for input/output operations.
    It is important to have DFS as global variable in this class to take advantatges of singeltons

    Info: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

    All pages can import this file and retrive data by:

        > from data_loader import DFS
        > df_xx = DFS[xx] # xx is the name of the dataframe
"""

import io

import dropbox
import pandas as pd
import oyaml as yaml

import constants as c
import utilities as u


DBX = dropbox.Dropbox(u.get_secret(c.io.VAR_DROPBOX_TOKEN))
DFS = {}
YML = {}


def get_config():
    """ retrives config yaml as ordered dict """

    _, res = DBX.files_download(c.io.FILE_CONFIG)
    return yaml.load(io.BytesIO(res.content), Loader=yaml.SafeLoader)


def get_money_lover_filename():
    """ gets the name of the money lover excel file """

    names = []

    # Explore all files and save all that are valid
    for x in DBX.files_list_folder(c.io.PATH_MONEY_LOVER).entries:
        try:
            # Try to parse date, if possible if a money lover file
            pd.to_datetime(x.name.split(".")[0])
            names.append(x.name)

        except (TypeError, ValueError):
            pass

    return max(names)


def get_df_transactions():
    """
        Retrives the df with transactions. It will read the newest money lover excel file

        Args:
            dbx:    dropbox connector needed to call the dropbox api

        Returns:
            raw dataframe with transactions
    """

    _, res = DBX.files_download(c.io.FILE_TRANSACTIONS)
    return pd.read_excel(io.BytesIO(res.content), index_col=0)


def get_data_without_transactions():
    """
        Retrives all dataframes from data.xlsx file

        Args:
            dbx:    dropbox connector needed to call the dropbox api

        Returns:
            dict with raw dataframes from data.xlsx file
    """
    _, res = DBX.files_download(c.io.FILE_DATA)

    dfs = {x: pd.read_excel(io.BytesIO(res.content), sheet_name=x) for x in c.dfs.ALL_FROM_DATA}

    return dfs


def sync():
    """ Retrives all dataframes and update DFS global var """

    DFS.update(get_data_without_transactions())
    DFS[c.dfs.TRANS] = get_df_transactions()

    YML.update(get_config())


# Do one sync when it is imported!
sync()
