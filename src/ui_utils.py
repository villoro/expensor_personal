"""
    Dash app
"""

import dash_html_components as html


PLOT_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["sendDataToCloud", "select2d", "lasso2d", "resetScale2d"]
}


def get_options(iterable):
    """
        Populates a dash dropdawn from an iterable
    """
    return [{"label": x, "value": x} for x in iterable]


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

    def __init__(self):
        self.show_drop_categories = False
        self.show_months_average = False
        self.show_grouping = False

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
