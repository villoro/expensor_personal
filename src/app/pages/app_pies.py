"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import utilities as u
import constants as c
from app import ui_utils as uiu
from plots import plots_pies as plots


class Page(uiu.AppPage):
    """ Page Pies """

    link = c.dash.LINK_PIES


    def __init__(self, dload, app):
        super().__init__(dload)

        self.all_years = self.gdf(c.dfs.TRANS)[c.cols.YEAR].unique().tolist()
        self.last_year_as_list = [max(self.all_years)]

        for num, _ in enumerate([self.all_years, self.last_year_as_list]):
            @app.callback(Output("plot_pie_{}_{}".format(num, c.names.INCOMES), "figure"),
                          [Input("drop_pie_categ", "value"),
                           Input("drop_pie_{}".format(num), "value")])
            #pylint: disable=unused-variable,unused-argument
            def update_pie_incomes(categories, years):
                """
                    Updates the incomes pie plot

                    Args:
                        categories: categories to use
                        years:      years to include in pie
                """
                df = u.dfs.filter_data(self.gdf(c.dfs.TRANS), categories)
                return plots.get_pie(df, self.gdf(c.dfs.CATEG), c.names.INCOMES, years)


            @app.callback(Output("plot_pie_{}_{}".format(num, c.names.EXPENSES), "figure"),
                          [Input("drop_pie_categ", "value"),
                           Input("drop_pie_{}".format(num), "value")])
            #pylint: disable=unused-variable,unused-argument
            def update_pie_expenses(categories, years):
                """
                    Updates the expenses pie plot

                    Args:
                        categories: categories to use
                        years:      years to include in pie
                """
                df = u.dfs.filter_data(self.gdf(c.dfs.TRANS), categories)
                return plots.get_pie(df, self.gdf(c.dfs.CATEG), c.names.EXPENSES, years)


    def get_body(self):
        body = []

        # Add plots and dropdowns
        # One row default with all data, the other with last year
        for num, myears in enumerate([self.all_years, self.last_year_as_list]):

            body.append(
                [
                    html.Div(
                        dcc.Dropdown(
                            id="drop_pie_{}".format(num), multi=True,
                            options=uiu.get_options(self.all_years),
                            # prevent long list selected
                            value=myears if myears != self.all_years else None
                        ), style=c.styles.get_style_wraper(10)
                    ),
                    uiu.get_row([
                        uiu.get_one_column(
                            dcc.Graph(
                                id="plot_pie_{}_{}".format(num, c.names.INCOMES),
                                config=uiu.PLOT_CONFIG,
                                figure=plots.get_pie(
                                    self.gdf(c.dfs.TRANS), self.gdf(c.dfs.CATEG),
                                    c.names.INCOMES, myears
                                )
                            ), n_rows=6
                        ),
                        uiu.get_one_column(
                            dcc.Graph(
                                id="plot_pie_{}_{}".format(num, c.names.EXPENSES),
                                config=uiu.PLOT_CONFIG,
                                figure=plots.get_pie(
                                    self.gdf(c.dfs.TRANS), self.gdf(c.dfs.CATEG),
                                    c.names.EXPENSES, myears
                                )
                            ), n_rows=6
                        )
                    ])
                ],
            )

        return body


    def get_filters(self):
        return [
            ("Categories", dcc.Dropdown(
                id="drop_pie_categ", multi=True,
                options=uiu.get_options(self.gdf(c.dfs.TRANS)[c.cols.CATEGORY].unique())
            ))
        ]
