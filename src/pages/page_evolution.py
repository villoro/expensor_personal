"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import utilities as u
import constants as c
import layout as lay
from plots import plots_evolution as plots
from data_loader import DFS


class Page(lay.AppPage):
    """ Page Evolution """

    link = c.dash.LINK_EVOLUTION
    def_type = c.names.EXPENSES
    def_tw = "M"


    def __init__(self, app):
        super().__init__([
            c.dash.INPUT_CATEGORIES,
            c.dash.INPUT_SMOOTHING,
            c.dash.INPUT_TIMEWINDOW
        ])

        @app.callback(Output("plot_evol", "figure"),
                      [Input("input_categories", "value"),
                       Input("input_timewindow", "value"),
                       Input("input_smoothing", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_timeserie_plot(categories, timewindow, avg_month):
            """
                Updates the timeserie plot

                Args:
                    categories: categories to use
                    timewindow: timewindow to use for grouping
                    avg_month:  month to use in time average
            """

            df = u.dfs.filter_data(DFS[c.dfs.TRANS], categories)
            return plots.plot_timeserie(df, timewindow, avg_month)


        @app.callback(Output("plot_evo_detail", "figure"),
                      [Input("input_categories", "value"),
                       Input("radio_evol_type", "value"),
                       Input("input_timewindow", "value"),
                       Input("input_smoothing", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_ts_by_categories_plot(categories, type_trans, timewindow, avg_month):
            """
                Updates the timeserie by categories plot

                Args:
                    categories: categories to use
                    type_trans: type of transacions [Expenses/Inc]
                    timewindow: timewindow to use for grouping
                    avg_month:  month to use in time average
            """
            df = u.dfs.filter_data(DFS[c.dfs.TRANS], categories)
            return plots.plot_timeserie_by_categories(
                df, DFS[c.dfs.CATEG], type_trans, timewindow, avg_month
            )

    def get_body(self):
        return [
            dcc.Graph(
                id="plot_evol", config=c.dash.PLOT_CONFIG,
                figure=plots.plot_timeserie(DFS[c.dfs.TRANS], self.def_tw)),
            [
                dcc.Graph(
                    id="plot_evo_detail", config=c.dash.PLOT_CONFIG,
                    figure=plots.plot_timeserie_by_categories(
                        DFS[c.dfs.TRANS], DFS[c.dfs.CATEG], self.def_type, self.def_tw
                    )
                ),
                dcc.RadioItems(
                    id="radio_evol_type",
                    options=lay.get_options([c.names.EXPENSES, c.names.INCOMES]),
                    value=self.def_type,
                    labelStyle={'display': 'inline-block'}
                )
            ],
        ]
