"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import utilities as u
import constants as c
from app import ui_utils as uiu
from plots import plots_heatmaps as plots


class Page(uiu.AppPage):
    """ Page Heatmaps """

    link = c.dash.LINK_HEATMAPS


    def __init__(self, dload, app):
        super().__init__(dload)

        @app.callback(Output("plot_heat_i", "figure"),
                      [Input("drop_heat_categ", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_heatmap_i(categories):
            """
                Updates the incomes heatmap

                Args:
                    categories: categories to use
            """
            df = u.dfs.filter_data(self.gdf(c.dfs.TRANS), categories)
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
            df = u.dfs.filter_data(self.gdf(c.dfs.TRANS), categories)
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
            df = u.dfs.filter_data(self.gdf(c.dfs.TRANS), categories)
            return plots.dist_plot(df)


    def get_body(self):
        return [
            [
                uiu.get_one_column(
                    dcc.Graph(
                        id="plot_heat_i", config=uiu.PLOT_CONFIG,
                        figure=plots.get_heatmap(self.gdf(c.dfs.TRANS), c.names.INCOMES)
                    ), n_rows=6
                ),
                uiu.get_one_column(
                    dcc.Graph(
                        id="plot_heat_e", config=uiu.PLOT_CONFIG,
                        figure=plots.get_heatmap(self.gdf(c.dfs.TRANS), c.names.EXPENSES)
                    ), n_rows=6
                )
            ],
            dcc.Graph(
                id="plot_heat_distribution", config=uiu.PLOT_CONFIG,
                figure=plots.dist_plot(self.gdf(c.dfs.TRANS))
            ),
        ]

    def get_sidebar(self):
        return [
            ("Categories", dcc.Dropdown(
                id="drop_heat_categ", multi=True,
                options=uiu.get_options(self.gdf(c.dfs.TRANS)[c.cols.CATEGORY].unique())
            ))
        ]
