"""
    Utilities for input/output operations
"""

import os
import io

import pandas as pd
import dropbox

import constants as c
from utilities.dfs import fix_df_trans


def get_dropbox_conector():
    """ Creates a dropbox connector using the dropbox api with a token """
    return dropbox.Dropbox(os.environ[c.io.VAR_DROPBOX_TOKEN])


def get_money_lover_filename(dbx=None):
    """ gets the name of the money lover excel file """

    if dbx is None:
        dbx = get_dropbox_conector()

    names = []

    # Explore all files and save all that are valid
    for x in dbx.files_list_folder(c.io.PATH_MONEY_LOVER).entries:
        try:
            # Try to parse date, if possible if a money lover file
            pd.to_datetime(x.name.split(".")[0])
            names.append(x.name)

        except (TypeError, ValueError):
            pass

    return max(names)


def get_df_transactions(dbx):
    """
        Retrives the df with transactions. It will read the newest money lover excel file

        Args:
            dbx:    dropbox connector needed to call the dropbox api

        Returns:
            raw dataframe with transactions
    """
    filename = get_money_lover_filename(dbx)

    _, res = dbx.files_download(c.io.PATH_MONEY_LOVER + filename)

    return pd.read_excel(io.BytesIO(res.content), index_col=0)


def get_data_without_transactions(dbx):
    """
        Retrives all dataframes from data.xlsx file

        Args:
            dbx:    dropbox connector needed to call the dropbox api

        Returns:
            dict with raw dataframes from data.xlsx file
    """
    _, res = dbx.files_download(c.io.FILE_DATA)

    dfs = {x: pd.read_excel(io.BytesIO(res.content), sheet_name=x) for x in c.dfs.ALL_FROM_DATA}

    return dfs


class DataLoader():
    """ Class that handles data """

    def __init__(self):
        """ Retrives all dataframes """
        dbx = get_dropbox_conector()
        self.dfs = get_data_without_transactions(dbx)
        self.dfs[c.dfs.TRANS] = fix_df_trans(get_df_transactions(dbx))


    def sync(self):
        """ It will force a data loading """
        self.__init__()


    def get_data(self):
        """ Returns the dict of dataframes """
        return self.dfs

    def gdf(self, name):
        """ Returns one dataframe """
        return self.dfs.get(name, None)
