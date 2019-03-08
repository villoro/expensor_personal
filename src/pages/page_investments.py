"""
    Dash app
"""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
import layout as lay
from plots import plots_investment as plots
from data_loader import DFS


class Page(lay.AppPage):
    """ Page Pies """

    link = c.dash.LINK_INVESTMENTS
    dict_types = {c.names.INVESTED: c.dfs.INVEST, c.names.WORTH: c.dfs.WORTH}
    def_smooth = False

    def __init__(self, app):
        super().__init__([c.dash.INPUT_SMOOTHING])

        @app.callback(
            [
                Output("plot_invest_detail", "figure"),
                Output("plot_invest_total_worth", "figure"),
                Output("plot_passive_income", "figure"),
                Output("plot_invest_performance", "figure"),
            ],
            [
                Input("radio_invest_wor_inv", "value"),
                Input("input_smoothing", "value"),
                Input("radio_invest_smooth", "value"),
            ],
        )
        # pylint: disable=unused-variable,unused-argument
        def update_plots(type_df, avg_month, smooth):
            """
                Updates the plots

                Args:
                    type_df:    invested/worth
                    avg_month:  month to use in time average
                    smooth:     bool to allow/disable passive smoothing
            """

            df = DFS[self.dict_types[type_df]]

            return (
                plots.invest_evolution_plot(df, avg_month),
                plots.total_worth_plot(DFS[c.dfs.LIQUID], DFS[c.dfs.WORTH], avg_month),
                plots.passive_income_vs_expenses(
                    DFS[c.dfs.WORTH], DFS[c.dfs.TRANS], avg_month, smooth
                ),
                plots.performance_plot(DFS[c.dfs.INVEST], DFS[c.dfs.WORTH], avg_month),
            )

    def get_body(self):
        body = [
            lay.card(
                dcc.Graph(
                    id="plot_invest_total_worth",
                    config=c.dash.PLOT_CONFIG,
                    figure=plots.total_worth_plot(
                        DFS[c.dfs.LIQUID], DFS[c.dfs.WORTH], c.dash.DEFAULT_SMOOTHING
                    ),
                )
            ),
            lay.card(
                [
                    dcc.Graph(
                        id="plot_passive_income",
                        config=c.dash.PLOT_CONFIG,
                        figure=plots.passive_income_vs_expenses(
                            DFS[c.dfs.WORTH],
                            DFS[c.dfs.TRANS],
                            c.dash.DEFAULT_SMOOTHING,
                            self.def_smooth,
                        ),
                    ),
                    dbc.RadioItems(
                        id="radio_invest_smooth",
                        options=[
                            {"label": "Don't smooth", "value": False},
                            {"label": "Smooth passive income", "value": True},
                        ],
                        value=self.def_smooth,
                        inline=True,
                    ),
                ]
            ),
            lay.card(
                dcc.Graph(
                    id="plot_invest_performance",
                    config=c.dash.PLOT_CONFIG,
                    figure=plots.total_worth_plot(
                        DFS[c.dfs.INVEST], DFS[c.dfs.WORTH], c.dash.DEFAULT_SMOOTHING
                    ),
                )
            ),
            lay.card(
                [
                    dcc.Graph(
                        id="plot_invest_detail",
                        config=c.dash.PLOT_CONFIG,
                        figure=plots.invest_evolution_plot(
                            DFS[c.dfs.INVEST], c.dash.DEFAULT_SMOOTHING
                        ),
                    ),
                    dbc.RadioItems(
                        id="radio_invest_wor_inv",
                        options=lay.get_options([c.names.WORTH, c.names.INVESTED]),
                        value=c.names.WORTH,
                        inline=True,
                    ),
                ]
            ),
        ]

        return body
