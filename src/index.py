"""
    Dash app
"""

from dash import callback_context
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
    [Output("body", "children"), Output("filters", "children")],
    [Input("url", "pathname"), Input("sync", "n_clicks")],
)
# pylint: disable=unused-variable
def change_page(pathname, _):
    """ Updates the page content """

    ctx = callback_context

    # If sync button pressed, sync the app
    if ctx.triggered and ctx.triggered[0]["prop_id"] == "sync.n_clicks":
        sync()

    page = PAGES.get(pathname, None)

    if page is not None:
        return page.get_body_html(), page.get_filters()
    return ["404"] * 2


@APP.callback(
    Output("filters-container", "is_open"),
    [Input("filters-button", "n_clicks")],
    [State("filters-container", "is_open")],
)
def toggle_filters(count, is_open):
    """ hides/opens the filter block """

    if count:
        return not is_open
    return is_open


if __name__ == "__main__":
    APP.run_server(debug=True)
