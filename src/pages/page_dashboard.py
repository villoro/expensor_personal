"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
import layout as lay
from plots import plots_evolution as plt_ev
from plots import plots_liquid as plt_li
from plots import plots_dashboard as plt_db
from plots import plots_investment as plt_inv

from data_loader import DFS


class Page(lay.AppPage):
    """ Page Dashboard """

    link = c.dash.LINK_DASHBOARD
    plot_height = 380

    def __init__(self, app):
        super().__init__({c.dash.INPUT_SMOOTHING: True})

        @app.callback(
            [
                Output(f"plot_dash_{x}", "figure")
                for x in ["evol", "total_worth", "l_vs_e", "liq_months"]
            ],
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
                plt_ev.plot_timeserie(
                    DFS[c.dfs.TRANS], avg_month=avg_month, height=self.plot_height
                ),
                plt_inv.total_worth_plot(
                    DFS[c.dfs.LIQUID], DFS[c.dfs.WORTH], avg_month, height=self.plot_height
                ),
                plt_li.plot_expenses_vs_liquid(
                    DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month, False, height=self.plot_height
                ),
                plt_li.plot_months(
                    DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month, False, height=self.plot_height
                ),
            )

    def get_body(self):
        return [
            plt_db.get_summary(DFS),
            lay.two_columns(
                [
                    lay.card(
                        dcc.Graph(
                            id="plot_dash_evol",
                            config=c.dash.PLOT_CONFIG,
                            figure=plt_ev.plot_timeserie(
                                DFS[c.dfs.TRANS],
                                avg_month=c.dash.DEFAULT_SMOOTHING,
                                height=self.plot_height,
                            ),
                        )
                    ),
                    lay.card(
                        dcc.Graph(
                            id="plot_dash_total_worth",
                            config=c.dash.PLOT_CONFIG,
                            figure=plt_inv.total_worth_plot(
                                DFS[c.dfs.LIQUID],
                                DFS[c.dfs.WORTH],
                                c.dash.DEFAULT_SMOOTHING,
                                height=self.plot_height,
                            ),
                        )
                    ),
                ]
            ),
            lay.two_columns(
                [
                    lay.card(
                        dcc.Graph(
                            id="plot_dash_l_vs_e",
                            config=c.dash.PLOT_CONFIG,
                            figure=plt_li.plot_expenses_vs_liquid(
                                DFS[c.dfs.LIQUID],
                                DFS[c.dfs.TRANS],
                                c.dash.DEFAULT_SMOOTHING,
                                False,
                                height=self.plot_height,
                            ),
                        )
                    ),
                    lay.card(
                        dcc.Graph(
                            id="plot_dash_liq_months",
                            config=c.dash.PLOT_CONFIG,
                            figure=plt_li.plot_months(
                                DFS[c.dfs.LIQUID],
                                DFS[c.dfs.TRANS],
                                c.dash.DEFAULT_SMOOTHING,
                                False,
                                height=self.plot_height,
                            ),
                        )
                    ),
                ]
            ),
        ]
