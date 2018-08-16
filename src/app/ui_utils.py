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


def _get_row_or_col(data, kwa, style):
    """ Auxiliar function to get row/column div """

    if style is not None:
        kwa["style"] = style

    return html.Div(data, **kwa)


def get_one_column(data, n_rows=12, style=None):
    """
        Creates one column that will contain the data

        Args:
            data:   what to put inside
            n_rows: width relative to a 12 column system
            style:  style for the row

        Returns:
            html div containg the data
    """

    kwa = {"className": "{} columns".format(c.dash.NUM_DICT[n_rows])}
    return _get_row_or_col(data, kwa, style)


def get_row(data, style=None):
    """
        Creates one row that will contain the data

        Args:
            data:   what to put inside
            style:  style for the row

        Returns:
            html div containg the data
    """
    return _get_row_or_col(data, {"className": "row"}, style)


def _get_sidebar_elem(title, data):
    """
        Creates an element for the sidebar

        Args:
            title:  name to display
            data:   what to include in the element

        Return:
            html div with the element
    """

    aux = html.H6(title + ":")
    children = [aux] + data if isinstance(data, list) else [aux, data]

    return html.Div(children, style=c.styles.SIDEBAR_ELEM)


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
    def get_sidebar(self):
        """ Dummy function to be overrided by every page. It should create the sidebar """
        return None

    def get_body_html(self):
        """ Retrives the html body """

        elem_style = c.styles.DIV_CONTROL_IN_BODY

        return [html.Div(data, className="row", style=elem_style) for data in self.get_body()]


    def get_sidebar_html(self):
        """ Retrives the html sidebar """

        elements = [
            ("Sections", [
                html.Div(dcc.Link(name, href=link)) for name, link in c.dash.DICT_APPS.items()]
            )
        ]

        sidebar = self.get_sidebar()

        # Finally add extra things in sidebar
        if sidebar is not None:
            elements += sidebar

        return [_get_sidebar_elem(title, data) for title, data in elements]
