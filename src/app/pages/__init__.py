"""
    Folder for all dash pages
"""

import os
import importlib
from dash.dependencies import Input, Output

import constants as c
from utilities.io import DataLoader
from app import ui_utils as uiu

def get_pages(app):
    """
        Creates all dash pages

        Args:
            app:    dash app

        Returns:
            Pages as a json with the next structure

            --page_link_1
                --conent
                --sidebar

            --page_link_n
                --content
                --sidebar
    """

    dload = DataLoader()

    @app.callback(Output("sync_count", "children"),
                  [Input("sync", "n_clicks")])
    #pylint: disable=unused-variable,unused-argument
    def update_sync_count(x):
        """
            Updates the liquid vs expenses plot

            Args:
                avg_month:  month to use in rolling average
        """
        dload.sync_data()

        return x

    output = {}
    for app_name in os.listdir("src/app/pages"):

        # Check if it is an app
        if (app_name.startswith("app")) and (app_name.endswith(".py")):

            # Fix app name
            app_name = ".{}".format(app_name.split(".")[0])

            # Import it programatically
            m_page = importlib.import_module(app_name, "app.pages").Page(dload, app)

            # Add content to the output dict
            output[m_page.link] = m_page

    # Clone content of the page that will appear in the root path
    output[c.dash.LINK_MAIN] = output[c.dash.LANDING_APP]

    return output
