
from dash import Dash
from dash.dependencies import Input, Output, State
from dash_bootstrap_components.themes import BOOTSTRAP

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import constants as c
from ui_utils import get_options
from data_loader import DFS


app = Dash('expensor_personal', external_stylesheets=[BOOTSTRAP])
app.config.supress_callback_exceptions = True

dropdown_items = [
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
    [
        #dbc.Button("Sync", id="sync", className="mr-1"),
        dbc.Button("Filters", outline=True, color="primary", id="collapse-button", className="mr-1")
    ] + dropdown_items,
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
            id='time_average',
            type='number',
            value=c.dash.DEFAULT_SMOOTHING,
        ),
    },
    # Time window
    {
        "title": "Grouping:",
        "size": {"xs": 12, "md": 6, "lg": 3},
        "data": dcc.Dropdown(
            id="drop_timewindow",
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
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dbc.FormGroup(
                        [
                            dbc.Label(x["title"], width=4),
                            dbc.Col(x["data"], width=8)
                        ], 
                        row=True, 
                        className="w3-card",
                        style={"padding-top": "8px", "padding-bottom": "8px"}
                    ),
                    style={"padding-left": "32px", "padding-right": "32px"}
                ),
                style={"padding-top": "16px"},
                **x["size"],
            ) for x in filters_data
        ],
        form=True,
    ),
    id="collapse",
    className="w3-padding-large"
)

content = [
    # Body
    html.Div(id="body", className="w3-padding-large w3-green"),

    # Others
    html.Div(id="sync_count", style={"display": "none"}),
    dcc.Location(id='url', refresh=False),
]

app.layout = html.Div([navbar, filters] + content)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)