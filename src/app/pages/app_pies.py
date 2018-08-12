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


LINK = c.dash.LINK_PIES


def get_content(app, dfs):
    """
        Creates the page

        Args:
            app:    dash app
            dfs:    dict with dataframes

        Returns:
            dict with content:
                body:       body of the page
    """

    sidebar = [
        ("Categories", dcc.Dropdown(
            id="drop_pie_categ", multi=True,
            options=uiu.get_options(dfs[c.dfs.TRANS][c.cols.CATEGORY].unique())
        ))
    ]

    content = []

    all_years = dfs[c.dfs.TRANS][c.cols.YEAR].unique().tolist()
    last_year_as_list = [max(all_years)]

    # Add plots and dropdowns
    # One row default with all data, the other with last year
    for num, myears in enumerate([all_years, last_year_as_list]):

        content.append(
            [
                html.Div(
                    dcc.Dropdown(
                        id="drop_pie_{}".format(num), multi=True,
                        options=uiu.get_options(all_years),
                        value=myears if myears != all_years else None # prevent long list selected
                    ), style=c.styles.get_style_wraper(10)
                ),
                uiu.get_row([
                    uiu.get_one_column(
                        dcc.Graph(
                            id="plot_pie_{}_{}".format(num, c.names.INCOMES),
                            config=uiu.PLOT_CONFIG,
                            figure=plots.get_pie(
                                dfs[c.dfs.TRANS], dfs[c.dfs.CATEG], c.names.INCOMES, myears
                            )
                        ), n_rows=6
                    ),
                    uiu.get_one_column(
                        dcc.Graph(
                            id="plot_pie_{}_{}".format(num, c.names.EXPENSES),
                            config=uiu.PLOT_CONFIG,
                            figure=plots.get_pie(
                                dfs[c.dfs.TRANS], dfs[c.dfs.CATEG], c.names.EXPENSES, myears
                            )
                        ), n_rows=6
                    )
                ])
            ],
        )


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
            df = u.dfs.filter_data(dfs[c.dfs.TRANS], categories)
            return plots.get_pie(df, dfs[c.dfs.CATEG], c.names.INCOMES, years)


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
            df = u.dfs.filter_data(dfs[c.dfs.TRANS], categories)
            return plots.get_pie(df, dfs[c.dfs.CATEG], c.names.EXPENSES, years)

    return {c.dash.KEY_BODY: content, c.dash.KEY_SIDEBAR: sidebar}
