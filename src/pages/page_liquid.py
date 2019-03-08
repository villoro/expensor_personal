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

        @app.callback(
            [Output(f"plot_heat_{x}", "figure") for x in ["evo", "vs_expenses", "months"]],
            [Input("input_smoothing", "value")],
        )
        # pylint: disable=unused-variable,unused-argument
        def update_plots(avg_month):
            """
                Updates the plots

                Args:
                    avg_month:  month to use in time average
            """

            return (
                plots.liquid_plot(DFS[c.dfs.LIQUID], avg_month),
                plots.plot_expenses_vs_liquid(DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month),
                plots.plot_months(DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month),
            )

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
