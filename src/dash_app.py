"""
    Dash app
"""

import os

import dash_auth
from dash import Dash

from app import layout

VALID_USERNAME_PASSWORD_PAIRS = [
    [os.environ["EXPENSOR_USER"], os.environ["EXPENSOR_PASSWORD"]]
]

def create_dash_app():
    """
        Creates the dash app and gets the related data
    """

    app = Dash('auth')
    app.config.supress_callback_exceptions = True

    auth = dash_auth.BasicAuth(
        app,
        VALID_USERNAME_PASSWORD_PAIRS
    )

    app.layout = layout.get_layout(None)

    return app
