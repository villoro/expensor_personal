"""
    Dash app
"""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import constants as c
from data_loader import DFS


def get_options(iterable):
    """
        Populates a dash dropdawn from an iterable
    """
    return [{"label": x, "value": x} for x in iterable]


FILTERS = {
    c.dash.SHOW_MONTH_AVERAGE: (
        "Smoothing:",
        dbc.Input(
            id='input_time_average',
            type='number',
            value=c.dash.DEFAULT_SMOOTHING,
        ),
    ),
    c.dash.SHOW_GROUPING: (
        "Grouping:",
        dcc.Dropdown(
            id="input_timewindow",
            value="M",
            options=[
                {"label": "Month ", "value": "M"},
                {"label": "Year ", "value": "Y"}
            ],
        ),
    ),
    c.dash.SHOW_CATEGORIES: (
        "Categories:",
        dcc.Dropdown(
            id="input_categories",
            multi=True,
            options=get_options(DFS[c.dfs.TRANS][c.cols.CATEGORY].unique())
        )
    )
}


PLOT_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["sendDataToCloud", "select2d", "lasso2d", "resetScale2d"]
}


def two_columns(elements):
    """
        Creates a layout with two columns.
        In large screens will be displayed as two columns.
        In medium and smalls will be shown as only one.
    """

    return html.Div(
        [
            html.Div(
                x, className="w3-col l6 m12 s12"
            ) for x in elements
        ],
        className="w3-row"
    )


class AppPage():
    """
        Raw Page class that is meant to be extended
    """

    def __init__(self, mlist=[]):
        self.filters = [FILTERS[x] for x in mlist]


    def get_filters(self):
        """ Retrives the html body """

        return [
            dbc.Card(
                [
                    dbc.CardHeader(title),
                    html.Div(element, className="w3-padding")
                ]
            ) for title, element in self.filters
        ]


    #pylint: disable=R0201
    def get_body(self):
        """ Dummy function to be overrided by every page. It should create the body """
        return []


    def get_body_html(self):
        """ Retrives the html body """

        return [
            html.Div(
                data, className="w3-card w3-padding-large w3-margin w3-center"
            ) for data in self.get_body()
        ]
