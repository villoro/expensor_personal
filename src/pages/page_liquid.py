"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
import ui_utils as uiu
from plots import plots_liquid as plots
from data_loader import DFS


class Page(uiu.AppPage):
    """ Page Liquid """

    link = c.dash.LINK_LIQUID
    def_ma = 12


    def __init__(self, app):
        super().__init__({
            c.dash.SHOW_MONTH_AVERAGE: True,
        })

        @app.callback(Output("plot_liquid_vs_expenses", "figure"),
                      [Input("input_time_average", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_liquid_vs_expenses(avg_month):
            """
                Updates the liquid vs expenses plot

                Args:
                    avg_month:  month to use in time average
            """

            return plots.plot_expenses_vs_liquid(
                DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month
            )


        @app.callback(Output("plot_liquid_months", "figure"),
                      [Input("input_time_average", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_liquid_months(avg_month):
            """
                Updates the survival months plot

                Args:
                    avg_month:  month to use in time average
            """

            return plots.plot_months(
                DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month
            )


    def get_body(self):
        return [
            dcc.Graph(
                id="plot_liquid_evo", config=uiu.PLOT_CONFIG,
                figure=plots.liquid_plot(DFS[c.dfs.LIQUID], DFS[c.dfs.LIQUID_LIST])
            ),
            dcc.Graph(
                id="plot_liquid_vs_expenses", config=uiu.PLOT_CONFIG,
                figure=plots.plot_expenses_vs_liquid(
                    DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], self.def_ma
                )
            ),
            dcc.Graph(
                id="plot_liquid_months", config=uiu.PLOT_CONFIG,
                figure=plots.plot_months(DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], self.def_ma)
            ),
        ]
