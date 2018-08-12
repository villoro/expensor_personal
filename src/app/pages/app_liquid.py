"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
from app import ui_utils as uiu
from plots import plots_liquid as plots


LINK = c.dash.LINK_LIQUID


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

    def_avg_month = 12

    content = [
        dcc.Graph(
            id="plot_liquid_evo", config=uiu.PLOT_CONFIG,
            figure=plots.liquid_plot(dfs[c.dfs.LIQUID], dfs[c.dfs.LIQUID_LIST])
        ),
        dcc.Graph(
            id="plot_liquid_vs_expenses", config=uiu.PLOT_CONFIG,
            figure=plots.plot_expenses_vs_liquid(dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], def_avg_month)
        ),
        dcc.Graph(
            id="plot_liquid_months", config=uiu.PLOT_CONFIG,
            figure=plots.plot_months(dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], def_avg_month)
        ),
    ]

    sidebar = [
        ("Rolling Average", dcc.Slider(
            id="slider_liq_rolling_avg",
            min=1, max=12, value=def_avg_month,
            marks={i: str(i) if i > 1 else "None" for i in range(1, 13)},
        ))
    ]

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
            dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], avg_month
        )

    @app.callback(Output("plot_liquid_months", "figure"),
                  [Input("slider_liq_rolling_avg", "value")])
    #pylint: disable=unused-variable,unused-argument
    def update_liquid_months(avg_month):
        """
            Updates the survival months plot

            Args:
                df_liq:     dataframe with liquid info
                df_trans:   dataframe with transactions
                avg_month:  month to use in rolling average
        """

        return plots.plot_months(
            dfs[c.dfs.LIQUID], dfs[c.dfs.TRANS], avg_month
        )

    return {c.dash.KEY_BODY: content, c.dash.KEY_SIDEBAR: sidebar}
