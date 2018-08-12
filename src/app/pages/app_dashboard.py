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


LINK = c.dash.LINK_DASHBOARD


def get_content(app, dfs):
    """
        Creates the page

        Args:
            app:    dash app
            dfs:    dict with dataframes

        Returns:
            dict with content:
                body:       body of the page
                sidebar:    content of the sidebar
    """

    def_ma = 12

    content = [
        [
            uiu.get_one_column(plt_db.get_summary(dfs), n_rows=4),
            uiu.get_one_column(
                dcc.Graph(
                    id="plot_dash_evol", config=uiu.PLOT_CONFIG,
                    figure=plt_ev.plot_timeserie(dfs[c.dfs.TRANS], avg_month=def_ma)
                ), n_rows=8
            ),
        ],
        [
            uiu.get_one_column(
                dcc.Graph(
                    id="plot_dash_l_vs_e", config=uiu.PLOT_CONFIG,
                    figure=plt_li.plot_expenses_vs_liquid(
                        dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], def_ma, False
                    )
                ), n_rows=7
            ),
            uiu.get_one_column(
                dcc.Graph(
                    id="plot_dash_liq_months", config=uiu.PLOT_CONFIG,
                    figure=plt_li.plot_months(dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], def_ma, False)
                ), n_rows=5
            )
        ],
    ]

    sidebar = [
        ("Rolling Average", dcc.Slider(
            id="slider_dash_rolling_avg",
            min=1, max=12, value=def_ma,
            marks={i: str(i) if i > 1 else "None" for i in range(1, 13)},
        ))
    ]


    @app.callback(Output("plot_dash_evol", "figure"),
                  [Input("slider_dash_rolling_avg", "value")])
    #pylint: disable=unused-variable,unused-argument
    def update_timeserie_plot(avg_month):
        """
            Updates the timeserie plot

            Args:
                avg_month:  month to use in rolling average
        """
        return plt_ev.plot_timeserie(dfs[c.dfs.TRANS], avg_month=avg_month)


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
            dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], avg_month, False
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
            dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], avg_month, False
        )

    return {c.dash.KEY_BODY: content, c.dash.KEY_SIDEBAR: sidebar}
