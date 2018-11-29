"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import utilities as u
import constants as c
from app import ui_utils as uiu
from plots import plots_heatmaps as plots
from data_loader import DFS


class Page(uiu.AppPage):
    """ Page Heatmaps """

    link = c.dash.LINK_HEATMAPS


    def __init__(self, app):

        @app.callback(Output("plot_heat_i", "figure"),
                      [Input("drop_heat_categ", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_heatmap_i(categories):
            """
                Updates the incomes heatmap

                Args:
                    categories: categories to use
            """
            df = u.dfs.filter_data(DFS[c.dfs.TRANS], categories)
            return plots.get_heatmap(df, c.names.INCOMES)


        @app.callback(Output("plot_heat_e", "figure"),
                      [Input("drop_heat_categ", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_heatmap_e(categories):
            """
                Updates the expenses heatmap

                Args:
                    categories: categories to use
            """
            df = u.dfs.filter_data(DFS[c.dfs.TRANS], categories)
            return plots.get_heatmap(df, c.names.EXPENSES)


        @app.callback(Output("plot_heat_distribution", "figure"),
                      [Input("drop_heat_categ", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_distplot(categories):
            """
                Updates the distribution plot

                Args:
                    categories: categories to use
            """
            df = u.dfs.filter_data(DFS[c.dfs.TRANS], categories)
            return plots.dist_plot(df)


    def get_body(self):
        return [
            html.Div(
                [
                    html.Div(
                        dcc.Graph(
                            id="plot_heat_i", config=uiu.PLOT_CONFIG,
                            figure=plots.get_heatmap(DFS[c.dfs.TRANS], c.names.INCOMES)
                        ),
                        className="w3-col l6 m6 s12"
                    ),
                    html.Div(
                        dcc.Graph(
                            id="plot_heat_e", config=uiu.PLOT_CONFIG,
                            figure=plots.get_heatmap(DFS[c.dfs.TRANS], c.names.EXPENSES)
                        ),
                        className="w3-col l6 m6 s12"
                    ),
                ],
                className="w3-row"
            ),
            dcc.Graph(
                id="plot_heat_distribution", config=uiu.PLOT_CONFIG,
                figure=plots.dist_plot(DFS[c.dfs.TRANS])
            ),
        ]

    def get_filters(self):
        return {
            "Categories":
                dcc.Dropdown(
                    id="drop_heat_categ", multi=True,
                    options=uiu.get_options(DFS[c.dfs.TRANS][c.cols.CATEGORY].unique())
                ),
        }
