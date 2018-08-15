"""
    Dash app
"""

from dash.dependencies import Input, Output

from app.pages import get_pages
from dash_app import create_dash_app

import constants as c


# Create dash app with styles
APP = create_dash_app()
SERVER = APP.server

# Add pages with content, sidebar and callbacks
PAGES = get_pages(APP)


@APP.callback(Output('body', 'children'),
              [Input('url', 'pathname')])
#pylint: disable=unused-variable
def display_content(pathname):
    """Updates content based on current page"""

    if pathname in PAGES:
        return PAGES[pathname][c.dash.KEY_BODY]
    return "404"


@APP.callback(Output('sidebar', 'children'),
              [Input('url', 'pathname')])
#pylint: disable=unused-variable
def display_sidebar(pathname):
    """Updates sidebar based on current page"""

    if pathname in PAGES:
        return PAGES[pathname][c.dash.KEY_SIDEBAR]
    return "404"


if __name__ == '__main__':
    APP.run_server(debug=True)
