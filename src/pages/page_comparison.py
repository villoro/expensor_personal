"""
    Dash app
"""

import dash_bootstrap_components as dbc
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
        super().__init__([c.dash.INPUT_CATEGORIES, c.dash.INPUT_SMOOTHING])

        @app.callback(
            [Output(f"plot_comp_{x}", "figure") for x in list("12")],
            [
                Input("input_categories", "value"),
                Input("input_smoothing", "value"),
                Input("radio_comp_1", "value"),
                Input("radio_comp_2", "value"),
            ],
        )
        # pylint: disable=unused-variable,unused-argument
        def update_plots(categories, avg_month, type_trans_1, type_trans_2):
            """
                Updates the plots

                Args:
                    categories: categories to use
                    avg_month:  month to use in time average
                    type_trans_1: expenses/incomes/ebit plot 1
                    type_trans_2: expenses/incomes/ebit plot 2
            """

            df = u.filter_data(DFS[c.dfs.TRANS], categories)
            return (
                plots.ts_gradient(df, type_trans_1, avg_month),
                plots.ts_gradient(df, type_trans_2, avg_month),
            )

    def get_body(self):
        return [
            lay.card(
                [
                    dcc.Graph(
                        id="plot_comp_1",
                        config=c.dash.PLOT_CONFIG,
                        figure=plots.ts_gradient(
                            DFS[c.dfs.TRANS], c.names.INCOMES, c.dash.DEFAULT_SMOOTHING
                        ),
                    ),
                    dbc.RadioItems(
                        id="radio_comp_1",
                        options=self.radio_opt,
                        value=c.names.INCOMES,
                        inline=True,
                    ),
                ]
            ),
            lay.card(
                [
                    dcc.Graph(
                        id="plot_comp_2",
                        config=c.dash.PLOT_CONFIG,
                        figure=plots.ts_gradient(
                            DFS[c.dfs.TRANS], c.names.EXPENSES, c.dash.DEFAULT_SMOOTHING
                        ),
                    ),
                    dbc.RadioItems(
                        id="radio_comp_2",
                        options=self.radio_opt,
                        value=c.names.EXPENSES,
                        inline=True,
                    ),
                ]
            ),
        ]
