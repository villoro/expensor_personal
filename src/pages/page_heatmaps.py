"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import utilities as u
import constants as c
import layout as lay
from plots import plots_heatmaps as plots
from data_loader import DFS


class Page(lay.AppPage):
    """ Page Heatmaps """

    link = c.dash.LINK_HEATMAPS


    def __init__(self, app):
        super().__init__([
            c.dash.SHOW_CATEGORIES
        ])

        @app.callback(Output("plot_heat_i", "figure"),
                      [Input("input_categories", "value")])
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
                      [Input("input_categories", "value")])
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
                      [Input("input_categories", "value")])
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
            lay.two_columns([
                dcc.Graph(
                    id="plot_heat_i", config=c.dash.PLOT_CONFIG,
                    figure=plots.get_heatmap(DFS[c.dfs.TRANS], c.names.INCOMES)
                ),
                dcc.Graph(
                    id="plot_heat_e", config=c.dash.PLOT_CONFIG,
                    figure=plots.get_heatmap(DFS[c.dfs.TRANS], c.names.EXPENSES)
                ),
            ]),
            dcc.Graph(
                id="plot_heat_distribution", config=c.dash.PLOT_CONFIG,
                figure=plots.dist_plot(DFS[c.dfs.TRANS])
            ),
        ]
