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
    c.dash.SHOW_MONTH_AVERAGE: (
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

def get_layout():
    """ Creates the dash layout """

    dropdown_items = [
        dbc.Button(
            "Sync", 
            id="sync",
            className="mr-1",
            outline=True,
            color="primary",
        ),
        dbc.Button(
            "Filters",
            id="filters-button",
            outline=True,
            color="primary",
            className="mr-1"
        ),
    ] + [
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Pages",
            children=[
                dbc.DropdownMenuItem(
                    x[1:], href=x, id="section_{}".format(x[1:]),
                ) for x in c.dash.LINKS_ALL
            ]
        ),
    ]

    navbar = dbc.Navbar(
        dropdown_items,
        brand="Expensor",
        brand_href="/",
        sticky="top",
    )

    filters = dbc.Collapse(
        dbc.CardDeck(id="filters"), id="filters-container", className="w3-padding-large"
    )

    content = [
        # Body
        html.Div(id="body", className="w3-padding-large"),

        # Others
        html.Div(id="sync_count", style={"display": "none"}),
        dcc.Location(id='url', refresh=False),
    ]

    return html.Div([navbar, filters] + content)
