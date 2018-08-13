"""
    Dash app
"""

import os

import dash_auth
from dash import Dash

import constants as c
from app import layout

VALID_USERNAME_PASSWORD_PAIRS = [
    [os.environ[c.io.VAR_USER], os.environ[c.io.VAR_PASSWORD]]
]

def create_dash_app():
    """
        Creates the dash app and gets the related data
    """

    app = Dash('auth')
    app.config.supress_callback_exceptions = True

    _ = dash_auth.BasicAuth(
        app,
        VALID_USERNAME_PASSWORD_PAIRS
    )

    app.title = c.names.TITLE
    app.layout = layout.get_layout()

    return app
