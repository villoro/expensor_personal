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


def create_sidebar(sidebar):
    """
        Creates the sidebar given a list of elements.
        Each element should have a title and some data
    """

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

        return html.Div(children, style=c.styles.STYLE_SIDEBAR_ELEM)

    elements = [
        ("Sections", [
            html.Div(dcc.Link(name, href=link)) for name, link in c.dash.DICT_APPS.items()]
        )
    ]

    # Finally add extra things in sidebar
    if sidebar is not None:
        elements += sidebar

    return [_get_sidebar_elem(title, data) for title, data in elements]


def create_body(datalist):
    """
        Creates an element for the body

        Args:
            datalist:   what to include in the body

        Return:
            html div with the element
    """

    elem_style = c.styles.STYLE_DIV_CONTROL_IN_BODY

    return [html.Div(data, className="row", style=elem_style) for data in datalist]


def get_one_column(data, n_rows=12):
    """
        Creates one column that will contain the data

        Args:
            data:   what to put inside
            n_rows: width relative to a 12 column system

        Returns:
            html div containg the data
    """

    return html.Div(data, className="{} columns".format(c.dash.NUM_DICT[n_rows]))


def get_row(data, style=None):
    """
        Creates one row that will contain the data

        Args:
            data:   what to put inside

        Returns:
            html div containg the data
    """

    kwa = None if style is None else {"style": style}
    return html.Div(data, className="row", **kwa)


class AppPage():

    def __init__(self, dload):
        self.dload = dload

    def gdf(self, name):
        return self.dload.dfs[name]

    def get_body(self):
        return None

    def get_sidebar(self):
        return None

    def get_body_html(self):
        return create_body(self.get_body())

    def get_sidebar_html(self):
        return create_sidebar(self.get_sidebar())
