"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html

import constants as c


PLOT_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["sendDataToCloud", "select2d", "lasso2d", "resetScale2d"]
}


def get_options(iterable):
    """
        Populates a dash dropdawn from an iterable
    """
    return [{"label": x, "value": x} for x in iterable]


class AppPage():
    """
        Raw Page class that is meant to be extended
    """

    def __init__(self, dload):
        self.dload = dload

    def gdf(self, name):
        """ Get one dataframe by it's name """
        return self.dload.gdf(name)

    #pylint: disable=R0201
    def get_body(self):
        """ Dummy function to be overrided by every page. It should create the body """
        return []

    #pylint: disable=R0201
    def get_filters(self):
        """ Dummy function to be overrided by every page. It should create the sidebar """
        return None

    def get_body_html(self):
        """ Retrives the html body """

        classes = "w3-card w3-padding-large w3-margin w3-center"

        return [html.Div(data, className=classes) for data in self.get_body()]


    def get_filters_html(self):
        """ Retrives the html filters """

        filters = self.get_filters()

        if filters is None:
            return []

        return [
            html.Div(
                html.Div(
                    html.H5(title),
                    className="w3-col l1 m2 s12"
                ),
                html.Div(
                    html.H1("Hello"),
                    className="w3-col l11 m10 s12"
                ),
                className="w3-row" 
            ) for title, data in filters.items()
        ]
