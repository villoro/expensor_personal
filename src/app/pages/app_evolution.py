"""
    Dash app
"""

import dash_core_components as dcc
from dash.dependencies import Input, Output

import utilities as u
import constants as c
from app import ui_utils as uiu
from plots import plots_evolution as plots


class Page(uiu.AppPage):
    """ Page Evolution """

    link = c.dash.LINK_EVOLUTION
    def_type = c.names.EXPENSES
    def_tw = "M"


    def __init__(self, dload, app):
        super().__init__(dload)

        @app.callback(Output("plot_evol", "figure"),
                      [Input("drop_evol_categ", "value"),
                       Input("radio_evol_tw", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_timeserie_plot(categories, timewindow):
            """
                Updates the timeserie plot

                Args:
                    categories: categories to use
                    timewindow: timewindow to use for grouping
            """
            df = u.dfs.filter_data(self.gdf(c.dfs.TRANS), categories)
            return plots.plot_timeserie(df, timewindow)


        @app.callback(Output("plot_evo_detail", "figure"),
                      [Input("drop_evol_categ", "value"),
                       Input("radio_evol_type", "value"),
                       Input("radio_evol_tw", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_ts_by_categories_plot(categories, type_trans, timewindow):
            """
                Updates the timeserie by categories plot

                Args:
                    categories: categories to use
                    type_trans: type of transacions [Expenses/Inc]
                    timewindow: timewindow to use for grouping
            """
            df = u.dfs.filter_data(self.gdf(c.dfs.TRANS), categories)
            return plots.plot_timeserie_by_categories(
                df, self.gdf(c.dfs.CATEG), type_trans, timewindow
            )

    def get_body(self):
        return [
            dcc.Graph(
                id="plot_evol", config=uiu.PLOT_CONFIG,
                figure=plots.plot_timeserie(self.gdf(c.dfs.TRANS), self.def_tw)),
            [
                dcc.Graph(
                    id="plot_evo_detail", config=uiu.PLOT_CONFIG,
                    figure=plots.plot_timeserie_by_categories(
                        self.gdf(c.dfs.TRANS), self.gdf(c.dfs.CATEG), self.def_type, self.def_tw
                    )
                ),
                dcc.RadioItems(
                    id="radio_evol_type",
                    options=uiu.get_options([c.names.EXPENSES, c.names.INCOMES]),
                    value=self.def_type,
                    labelStyle={'display': 'inline-block'}
                )
            ],
        ]

    def get_filters(self):
        return {
            "Categories":
                dcc.Dropdown(
                    id="drop_evol_categ", multi=True,
                    options=uiu.get_options(self.gdf(c.dfs.TRANS)[c.cols.CATEGORY].unique())
                ),
            "Group by":
                dcc.RadioItems(
                    id="radio_evol_tw", value=self.def_tw,
                    options=[{"label": "Day", "value": "D"},
                             {"label": "Month", "value": "M"},
                             {"label": "Year", "value": "Y"}]
                ),
        }
