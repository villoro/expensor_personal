"""
    Toggle callbacks
"""

from dash.dependencies import Input, Output, State

import constants as c


def add_toggle_callbacks(app, pages):
    """ add all toggle callbacks """

    def _dict_show_hide(pathname, key):
        """ Retrives html style to show or hide """
        if pathname in pages:
            return c.dash.SHOW_DICT(pages[pathname].show_dict.get(key, False))
        return {}

    @app.callback(
        Output("filters", 'style'), [Input('url', 'pathname')], [State('sync_count', 'children')]
    )
    #pylint: disable=unused-variable
    def toggle_categories(pathname, _):
        """Show or hide categories filters"""
        return _dict_show_hide(pathname, c.dash.SHOW_CATEGORIES)

    @app.callback(
        Output("title_time_average", 'style'),
        [Input('url', 'pathname')], [State('sync_count', 'children')]
    )
    #pylint: disable=unused-variable
    def toggle_month_average_title(pathname, _):
        """Show or hide month_average_title filters"""
        return _dict_show_hide(pathname, c.dash.SHOW_MONTH_AVERAGE)

    @app.callback(
        Output("input_time_average", 'style'),
        [Input('url', 'pathname')], [State('sync_count', 'children')]
    )
    #pylint: disable=unused-variable
    def toggle_month_average_input(pathname, _):
        """Show or hide month_average_input filters"""
        return _dict_show_hide(pathname, c.dash.SHOW_MONTH_AVERAGE)

    @app.callback(
        Output("title_timewindow", 'style'),
        [Input('url', 'pathname')], [State('sync_count', 'children')]
    )
    #pylint: disable=unused-variable
    def toggle_grouping_title(pathname, _):
        """Show or hide grouping_title filters"""
        return _dict_show_hide(pathname, c.dash.SHOW_GROUPING)

    @app.callback(
        Output("radio_timewindow", 'style'),
        [Input('url', 'pathname')], [State('sync_count', 'children')]
    )
    #pylint: disable=unused-variable
    def toggle_grouping_radio(pathname, _):
        """Show or hide grouping_radio filters"""
        return _dict_show_hide(pathname, c.dash.SHOW_GROUPING)
