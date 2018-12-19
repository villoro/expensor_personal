"""
    Dash app
"""

from dash.dependencies import Input, Output, State

from pages import get_pages
from dash_app import create_dash_app
from data_loader import sync


# Create dash app with styles
APP = create_dash_app()
SERVER = APP.server

# Add pages with content, sidebar and callbacks
PAGES = get_pages(APP)


@APP.callback(
    Output('body', 'children'),
    [Input('url', 'pathname')],
    [State('sync_count', 'children')]
)
#pylint: disable=unused-variable
def display_content(pathname, _):
    """ Updates content based on current page """

    if pathname in PAGES:
        return PAGES[pathname].get_body_html()
    return "404"


@APP.callback(
    Output("sync_count", "children"),
    [Input("sync", "n_clicks")]
)
#pylint: disable=unused-variable,unused-argument
def update_sync_count(x):
    """ sync data using the data_loader function """

    sync()
    return x



if __name__ == '__main__':
    APP.run_server(debug=True)
