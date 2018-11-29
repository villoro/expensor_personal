"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
from app import ui_utils as uiu
from plots import plots_liquid as plots
from data_loader import DFS


class Page(uiu.AppPage):
    """ Page Liquid """

    link = c.dash.LINK_LIQUID
    def_ma = 12


    def __init__(self, app):
        super().__init__()

        @app.callback(Output("plot_liquid_vs_expenses", "figure"),
                      [Input("slider_liq_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_liquid_vs_expenses(avg_month):
            """
                Updates the liquid vs expenses plot

                Args:
                    avg_month:  month to use in rolling average
            """

            return plots.plot_expenses_vs_liquid(
                DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month
            )


        @app.callback(Output("plot_liquid_months", "figure"),
                      [Input("slider_liq_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_liquid_months(avg_month):
            """
                Updates the survival months plot

                Args:
                    avg_month:  month to use in rolling average
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


    def get_filters(self):
        return {
            "Rolling Average":
                dcc.Slider(
                    id="slider_liq_rolling_avg",
                    min=1, max=12, value=self.def_ma,
                    marks={i: str(i) if i > 1 else "None" for i in range(1, 13)},
                )
        }
