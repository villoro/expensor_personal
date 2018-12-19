"""
    Dash app
"""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import constants as c
from ui_utils import get_options
from data_loader import DFS

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

    filters_data = [
        # Time average
        {
            "title": "Smoothing:",
            "size": {"xs": 12, "md": 6, "lg": 3},
            "data": dbc.Input(
                id='input_time_average',
                type='number',
                value=c.dash.DEFAULT_SMOOTHING,
            ),
        },
        # Time window
        {
            "title": "Grouping:",
            "size": {"xs": 12, "md": 6, "lg": 3},
            "data": dcc.Dropdown(
                id="radio_timewindow",
                value="M",
                options=[
                    {"label": "Month ", "value": "M"},
                    {"label": "Year ", "value": "Y"}
                ],
            ),
        },
        # Categories
        {
            "title": "Categories:",
            "size": {"xs": 12, "md": 12, "lg": 6},
            "data": dcc.Dropdown(
                id="drop_categories",
                multi=True,
                options=get_options(DFS[c.dfs.TRANS][c.cols.CATEGORY].unique())
            )
        }
    ]

    filters = dbc.Collapse(
        dbc.CardDeck(
            [
                dbc.Card(
                    [
                        dbc.CardHeader(x["title"]),
                        html.Div(
                            x["data"],
                            className="w3-padding"
                        )
                    ]
                ) for x in filters_data
            ],
        ),
        id="filters",
        className="w3-padding-large"
    )

    content = [
        # Body
        html.Div(id="body", className="w3-padding-large"),

        # Others
        html.Div(id="sync_count", style={"display": "none"}),
        dcc.Location(id='url', refresh=False),
    ]

    return html.Div([navbar, filters] + content)
