"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import constants as c
import ui_utils as uiu
from plots import plots_investment as plots
from data_loader import DFS


class Page(uiu.AppPage):
    """ Page Pies """

    link = c.dash.LINK_INVESTMENTS
    def_ma = 1
    dict_types = {c.names.INVESTED: c.dfs.INVEST, c.names.WORTH: c.dfs.WORTH}

    def __init__(self, app):
        super().__init__({
            c.dash.SHOW_MONTH_AVERAGE: True,
        })

        @app.callback(Output("plot_invest_detail", "figure"),
                      [Input("radio_invest", "value"),
                       Input("input_time_average", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_plot_invest(type_df, avg_month):
            """
                Updates the timeserie gradient plot

                Args:
                    type_df:    invested/worth
                    avg_month:  month to use in rolling average
            """



            df = DFS[self.dict_types[type_df]]

            return plots.invest_evolution_plot(df, avg_month)


        @app.callback(Output("plot_invest_total_worth", "figure"),
                      [Input("input_time_average", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_plot_total_worth(avg_month):
            """
                Updates the timeserie gradient plot

                Args:
                    avg_month:  month to use in rolling average
            """

            return plots.total_worth_plot(
                DFS[c.dfs.LIQUID], DFS[c.dfs.WORTH], avg_month
            )


    def get_body(self):
        body = [
            [
                dcc.Graph(
                    id="plot_invest_detail", config=uiu.PLOT_CONFIG,
                    figure=plots.invest_evolution_plot(DFS[c.dfs.INVEST], self.def_ma)
                ),
                dcc.RadioItems(
                    id="radio_invest", options=uiu.get_options([c.names.INVESTED, c.names.WORTH]),
                    value=c.names.INVESTED, labelStyle={'display': 'inline-block'}
                )
            ],
            dcc.Graph(
                id="plot_invest_total_worth", config=uiu.PLOT_CONFIG,
                figure=plots.total_worth_plot(
                    DFS[c.dfs.LIQUID], DFS[c.dfs.WORTH], self.def_ma
                )
            ),
        ]

        return body