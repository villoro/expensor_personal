"""
    Dash app
"""

import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event

import constants as c
import utilities as u
from app import ui_utils as uiu


LINK = c.dash.LINK_UPLOAD

STYLE_PADDING_VERTICAL = {"margin-top": "{}px".format(c.styles.PADDING_V)}

DICT_SHOW = {
    True: STYLE_PADDING_VERTICAL,
    False: c.styles.STYLE_HIDDEN,
}


def get_content(app):
    """
        Creates the page

        Args:
            app:        dash app

        Returns:
            dict with content:
                body:       body of the page
                sidebar:    content of the sidebar
    """

    content = [
        html.Div([
            dcc.Upload(
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select a File')
                ]),
                style=c.styles.STYLE_UPLOAD_CONTAINER,
                id="upload_container"
            ),
            html.Button('Use this file', id='upload_button', style=STYLE_PADDING_VERTICAL),
        ]),
        html.Div(id="upload_results", style=DICT_SHOW[True])
    ]

    return {c.dash.KEY_BODY: content}
