"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import utilities as u
import constants as c
import layout as lay
from plots import plots_comparison as plots
from data_loader import DFS


class Page(lay.AppPage):
    """ Page Comparison """

    link = c.dash.LINK_COMPARISON
    radio_opt = lay.get_options([c.names.INCOMES, c.names.EXPENSES, c.names.EBIT])


    def __init__(self, app):
        super().__init__([
            c.dash.SHOW_CATEGORIES,
            c.dash.SHOW_MONTH_AVERAGE,
        ])

        @app.callback(Output("plot_comp_1", "figure"),
                      [Input("input_categories", "value"),
                       Input("input_time_average", "value"),
                       Input("radio_comp_1", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_ts_grad_1(categories, avg_month, type_trans):
            """
                Updates the timeserie gradient plot

                Args:
                    categories: categories to use
                    avg_month:  month to use in time average
                    type_trans: expenses/incomes
            """

            df = u.dfs.filter_data(DFS[c.dfs.TRANS], categories)
            return plots.ts_gradient(df, type_trans, avg_month)


        @app.callback(Output("plot_comp_2", "figure"),
                      [Input("input_categories", "value"),
                       Input("input_time_average", "value"),
                       Input("radio_comp_2", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_ts_grad_2(categories, avg_month, type_trans):
            """
                Updates the timeserie gradient plot

                Args:
                    categories: categories to use
                    avg_month:  month to use in time average
                    type_trans: expenses/incomes
            """

            df = u.dfs.filter_data(DFS[c.dfs.TRANS], categories)
            return plots.ts_gradient(df, type_trans, avg_month)


    def get_body(self):
        return [
            [
                dcc.Graph(
                    id="plot_comp_1", config=c.dash.PLOT_CONFIG,
                    figure=plots.ts_gradient(
                        DFS[c.dfs.TRANS], c.names.INCOMES, c.dash.DEFAULT_SMOOTHING
                    )
                ),
                dcc.RadioItems(
                    id="radio_comp_1", options=self.radio_opt,
                    value=c.names.INCOMES, labelStyle={'display': 'inline-block'}
                )
            ],
            [
                dcc.Graph(
                    id="plot_comp_2", config=c.dash.PLOT_CONFIG,
                    figure=plots.ts_gradient(
                        DFS[c.dfs.TRANS], c.names.EXPENSES, c.dash.DEFAULT_SMOOTHING
                    )
                ),
                dcc.RadioItems(
                    id="radio_comp_2", options=self.radio_opt,
                    value=c.names.EXPENSES, labelStyle={'display': 'inline-block'}
                )
            ]
        ]
