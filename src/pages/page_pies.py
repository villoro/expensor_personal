"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import utilities as u
import constants as c
import layout as lay
from plots import plots_pies as plots
from data_loader import DFS


class Page(lay.AppPage):
    """ Page Pies """

    link = c.dash.LINK_PIES

    def __init__(self, app):
        super().__init__([c.dash.INPUT_CATEGORIES])

        self.all_years = DFS[c.dfs.TRANS][c.cols.YEAR].unique().tolist()
        self.last_year_as_list = [max(self.all_years)]

        for num, _ in enumerate([self.all_years, self.last_year_as_list]):

            @app.callback(
                [
                    Output("plot_pie_{}_{}".format(num, c.names.INCOMES), "figure"),
                    Output("plot_pie_{}_{}".format(num, c.names.EXPENSES), "figure"),
                ],
                [Input("input_categories", "value"), Input("drop_pie_{}".format(num), "value")],
            )
            # pylint: disable=unused-variable,unused-argument
            def update_pies(categories, years):
                """
                    Updates the pies plot

                    Args:
                        categories: categories to use
                        years:      years to include in pie
                """
                df = u.filter_data(DFS[c.dfs.TRANS], categories)
                return (
                    plots.get_pie(df, DFS[c.dfs.CATEG], c.names.INCOMES, years),
                    plots.get_pie(df, DFS[c.dfs.CATEG], c.names.EXPENSES, years),
                )

    def get_body(self):
        body = []

        # Add plots and dropdowns
        # One row default with all data, the other with last year
        for num, myears in enumerate([self.all_years, self.last_year_as_list]):

            body.append(
                lay.card(
                    [
                        html.Div(
                            dcc.Dropdown(
                                id="drop_pie_{}".format(num),
                                multi=True,
                                options=lay.get_options(self.all_years),
                                # prevent long list selected
                                value=myears if myears != self.all_years else None,
                            )
                        ),
                        lay.two_columns(
                            [
                                dcc.Graph(
                                    id="plot_pie_{}_{}".format(num, c.names.INCOMES),
                                    config=c.dash.PLOT_CONFIG,
                                    figure=plots.get_pie(
                                        DFS[c.dfs.TRANS], DFS[c.dfs.CATEG], c.names.INCOMES, myears
                                    ),
                                ),
                                dcc.Graph(
                                    id="plot_pie_{}_{}".format(num, c.names.EXPENSES),
                                    config=c.dash.PLOT_CONFIG,
                                    figure=plots.get_pie(
                                        DFS[c.dfs.TRANS], DFS[c.dfs.CATEG], c.names.EXPENSES, myears
                                    ),
                                ),
                            ]
                        ),
                    ]
                )
            )

        return body
