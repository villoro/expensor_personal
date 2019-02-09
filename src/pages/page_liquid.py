"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
import layout as lay
from plots import plots_liquid as plots
from data_loader import DFS


class Page(lay.AppPage):
    """ Page Liquid """

    link = c.dash.LINK_LIQUID

    def __init__(self, app):
        super().__init__([c.dash.INPUT_SMOOTHING])

        @app.callback(Output("plot_liquid_evo", "figure"), [Input("input_smoothing", "value")])
        # pylint: disable=unused-variable,unused-argument
        def update_liquid(avg_month):
            """
                Updates the liquid plot

                Args:
                    avg_month:  month to use in time average
            """

            return plots.liquid_plot(DFS[c.dfs.LIQUID], avg_month)

        @app.callback(
            Output("plot_liquid_vs_expenses", "figure"), [Input("input_smoothing", "value")]
        )
        # pylint: disable=unused-variable,unused-argument
        def update_liquid_vs_expenses(avg_month):
            """
                Updates the liquid vs expenses plot

                Args:
                    avg_month:  month to use in time average
            """

            return plots.plot_expenses_vs_liquid(DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month)

        @app.callback(Output("plot_liquid_months", "figure"), [Input("input_smoothing", "value")])
        # pylint: disable=unused-variable,unused-argument
        def update_liquid_months(avg_month):
            """
                Updates the survival months plot

                Args:
                    avg_month:  month to use in time average
            """

            return plots.plot_months(DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month)

    def get_body(self):
        return [
            lay.card(
                dcc.Graph(
                    id="plot_liquid_evo",
                    config=c.dash.PLOT_CONFIG,
                    figure=plots.liquid_plot(DFS[c.dfs.LIQUID], c.dash.DEFAULT_SMOOTHING),
                )
            ),
            lay.card(
                dcc.Graph(
                    id="plot_liquid_vs_expenses",
                    config=c.dash.PLOT_CONFIG,
                    figure=plots.plot_expenses_vs_liquid(
                        DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], c.dash.DEFAULT_SMOOTHING
                    ),
                )
            ),
            lay.card(
                dcc.Graph(
                    id="plot_liquid_months",
                    config=c.dash.PLOT_CONFIG,
                    figure=plots.plot_months(
                        DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], c.dash.DEFAULT_SMOOTHING
                    ),
                )
            ),
        ]
