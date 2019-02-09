"""
    Dash app
"""

import os

import dash_auth
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

import constants as c
import layout

VALID_USERNAME_PASSWORD_PAIRS = [[os.environ[c.io.VAR_USER], os.environ[c.io.VAR_PASSWORD]]]


def create_dash_app():
    """
        Creates the dash app and gets the related data
    """

    app = Dash("expensor_personal", external_stylesheets=[BOOTSTRAP])
    app.config.supress_callback_exceptions = True

    _ = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

    app.title = c.names.TITLE
    app.layout = layout.get_layout()

    return app
