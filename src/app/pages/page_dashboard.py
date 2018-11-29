"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import constants as c
from app import ui_utils as uiu
from plots import plots_evolution as plt_ev
from plots import plots_liquid as plt_li
from plots import plots_dashboard as plt_db
from plots import plots_investment as plt_inv

from data_loader import DFS


class Page(uiu.AppPage):
    """ Page Dashboard """

    link = c.dash.LINK_DASHBOARD
    def_ma = 12


    def __init__(self, app):

        @app.callback(Output("plot_dash_evol", "figure"),
                      [Input("slider_dash_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_timeserie_plot(avg_month):
            """
                Updates the timeserie plot

                Args:
                    avg_month:  month to use in rolling average
            """
            return plt_ev.plot_timeserie(DFS[c.dfs.TRANS], avg_month=avg_month)


        @app.callback(Output("plot_dash_l_vs_e", "figure"),
                      [Input("slider_dash_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_liquid_vs_expenses(avg_month):
            """
                Updates the liquid vs expenses plot

                Args:
                    avg_month:  month to use in rolling average
            """

            return plt_li.plot_expenses_vs_liquid(
                DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month, False
            )


        @app.callback(Output("plot_dash_liq_months", "figure"),
                      [Input("slider_dash_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_liquid_months(avg_month):
            """
                Updates the survival months plot

                Args:
                    avg_month:  month to use in rolling average
            """

            return plt_li.plot_months(
                DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], avg_month, False
            )

        @app.callback(Output("plot_dash_total_worth", "figure"),
                      [Input("slider_dash_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_plot_total_worth(avg_month):
            """
                Updates the timeserie gradient plot

                Args:
                    avg_month:  month to use in rolling average
            """

            return plt_inv.total_worth_plot(
                DFS[c.dfs.LIQUID], DFS[c.dfs.WORTH], avg_month
            )


    def get_body(self):
        return [
            plt_db.get_summary(DFS),
            html.Div(
                [
                    html.Div(
                        dcc.Graph(
                            id="plot_dash_evol", config=uiu.PLOT_CONFIG,
                            figure=plt_ev.plot_timeserie(DFS[c.dfs.TRANS], avg_month=self.def_ma)
                        ),
                        className="w3-col l6 m6 s12"
                    ),
                    html.Div(
                        dcc.Graph(
                            id="plot_dash_total_worth", config=uiu.PLOT_CONFIG,
                            figure=plt_inv.total_worth_plot(
                                DFS[c.dfs.LIQUID], DFS[c.dfs.WORTH], self.def_ma
                            )
                        ),
                        className="w3-col l6 m6 s12"
                    ),
                ],
                className="w3-row"
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Graph(
                            id="plot_dash_l_vs_e", config=uiu.PLOT_CONFIG,
                            figure=plt_li.plot_expenses_vs_liquid(
                                DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], self.def_ma, False
                            )
                        ),
                        className="w3-col l6 m6 s12"
                    ),
                    html.Div(
                        dcc.Graph(
                            id="plot_dash_liq_months", config=uiu.PLOT_CONFIG,
                            figure=plt_li.plot_months(
                                DFS[c.dfs.LIQUID], DFS[c.dfs.TRANS], self.def_ma, False
                            )
                        ),
                        className="w3-col l6 m6 s12"
                    )
                ],
                className="w3-row"
            )
        ]


    def get_filters(self):
        return {
            "Rolling Average":
                dcc.Slider(
                    id="slider_dash_rolling_avg",
                    min=1, max=12, value=self.def_ma,
                    marks={i: str(i) if i > 1 else "None" for i in range(1, 13)},
                ),
        }
