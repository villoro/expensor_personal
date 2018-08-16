"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
from app import ui_utils as uiu
from plots import plots_evolution as plt_ev
from plots import plots_liquid as plt_li
from plots import plots_dashboard as plt_db


class Page(uiu.AppPage):

    link = c.dash.LINK_DASHBOARD
    def_ma = 12

    def __init__(self, dload, app):
        super().__init__(dload)

        @app.callback(Output("plot_dash_evol", "figure"),
                      [Input("slider_dash_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_timeserie_plot(avg_month):
            """
                Updates the timeserie plot

                Args:
                    avg_month:  month to use in rolling average
            """
            return plt_ev.plot_timeserie(self.gdf(c.dfs.TRANS), avg_month=avg_month)


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
                self.gdf(c.dfs.LIQUID), self.gdf(c.dfs.TRANS), avg_month, False
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
                self.gdf(c.dfs.LIQUID), self.gdf(c.dfs.TRANS), avg_month, False
            )

    def get_body(self):
        return [
            [
                uiu.get_one_column(plt_db.get_summary(self.dload.dfs), n_rows=4),
                uiu.get_one_column(
                    dcc.Graph(
                        id="plot_dash_evol", config=uiu.PLOT_CONFIG,
                        figure=plt_ev.plot_timeserie(self.gdf(c.dfs.TRANS), avg_month=self.def_ma)
                    ), n_rows=8
                ),
            ],
            [
                uiu.get_one_column(
                    dcc.Graph(
                        id="plot_dash_l_vs_e", config=uiu.PLOT_CONFIG,
                        figure=plt_li.plot_expenses_vs_liquid(
                            self.gdf(c.dfs.LIQUID), self.gdf(c.dfs.TRANS), self.def_ma, False
                        )
                    ), n_rows=7
                ),
                uiu.get_one_column(
                    dcc.Graph(
                        id="plot_dash_liq_months", config=uiu.PLOT_CONFIG,
                        figure=plt_li.plot_months(
                            self.gdf(c.dfs.LIQUID), self.gdf(c.dfs.TRANS), self.def_ma, False
                        )
                    ), n_rows=5
                )
            ],
        ]

    def get_sidebar(self):
        return [
            ("Rolling Average", dcc.Slider(
                id="slider_dash_rolling_avg",
                min=1, max=12, value=self.def_ma,
                marks={i: str(i) if i > 1 else "None" for i in range(1, 13)},
            ))
        ]
