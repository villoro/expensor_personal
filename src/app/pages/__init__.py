"""
    Folder for all dash pages
"""

import os
import importlib

import constants as c
from app import ui_utils as uiu


def get_pages(app, dfs):
    """
        Creates all dash pages

        Args:
            app:    dash app
            dfs:    dict with dataframes

        Returns:
            Pages as a json with the next structure

            --page_link_1
                --conent
                --sidebar

            --page_link_n
                --content
                --sidebar
    """

    output = {}
    for app_name in os.listdir("src/app/pages"):

        # Check if it is an app
        if (app_name.startswith("app")) and (app_name.endswith(".py")):

            # Fix app name
            app_name = ".{}".format(app_name.split(".")[0])

            # Import it programatically
            m_app = importlib.import_module(app_name, "app.pages")

            # Retrive content from the page
            content = m_app.get_content(app, dfs)

            # Construct body and sidebar
            body = uiu.create_body(content[c.dash.KEY_BODY])
            sidebar = uiu.create_sidebar(content)

            # Add content to the output dict
            output[m_app.LINK] = {c.dash.KEY_BODY: body, c.dash.KEY_SIDEBAR: sidebar}

    # Clone content of the page that will appear in the root path
    output[c.dash.LINK_MAIN] = output[c.dash.LANDING_APP]

    return output
