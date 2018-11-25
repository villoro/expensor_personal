"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import utilities as u
import constants as c
from app import ui_utils as uiu
from plots import plots_investment as plots


class Page(uiu.AppPage):
    """ Page Pies """

    link = c.dash.LINK_INVESTMENTS
    def_ma = 1
    dict_types = {c.names.INVESTED: c.dfs.INVEST, c.names.WORTH: c.dfs.WORTH}

    def __init__(self, dload, app):
        super().__init__(dload)

        @app.callback(Output("plot_invest_detail", "figure"),
                      [Input("radio_invest", "value"),
                       Input("slider_invest_rolling_avg", "value")])
        #pylint: disable=unused-variable,unused-argument
        def update_plot_invest(type_df, avg_month):
            """
                Updates the timeserie gradient plot

                Args:
                    type_df:    invested/worth
                    avg_month:  month to use in rolling average
            """



            df = self.gdf(self.dict_types[type_df])

            return plots.invest_evolution_plot(df, avg_month)


    def get_body(self):
        body = [
            [
                dcc.Graph(
                    id="plot_invest_detail", config=uiu.PLOT_CONFIG,
                    figure=plots.invest_evolution_plot(self.gdf(c.dfs.INVEST), self.def_ma)
                ),
                dcc.RadioItems(
                    id="radio_invest", options=uiu.get_options([c.names.INVESTED, c.names.WORTH]),
                    value=c.names.INVESTED, labelStyle={'display': 'inline-block'}
                )
            ],
            dcc.Graph(
                id="plot_invest_with_liquid", config=uiu.PLOT_CONFIG,
                figure=plots.invest_evolution_plot(
                    self.gdf(c.dfs.LIQUID), self.gdf(c.dfs.WORTH), self.def_ma
                )
            ),
        ]

        return body


    def get_sidebar(self):
        return [
            ("Rolling Average", dcc.Slider(
                id="slider_invest_rolling_avg",
                min=1, max=12, value=self.def_ma,
                marks={i: str(i) if i > 1 else "None" for i in range(1, 13)},
            ))
        ]
