"""
	Individual plots
"""

from calendar import month_abbr  # options: [month_name, month_abbr]
from plotly import figure_factory as FF
import plotly.graph_objs as go

import constants as c
import utilities as u


def get_heatmap(dfg, type_trans):
    """
        Creates a heatmap with expenses or incomes

        Args:
            dfg:        dataframe to use
            type_trans: type of transaction [Income/Expense]

        Returns:
            the plotly plot as html-div format
    """

    df = u.group_df_by(dfg[dfg[c.cols.TYPE] == type_trans], "M")

    # No data no fun
    if df.shape[0] < 2:
        return {}

    df[c.cols.YEAR], df[c.cols.MONTH_DATE] = df.index.year, df.index.month

    df = df.pivot(c.cols.MONTH_DATE, c.cols.YEAR, c.cols.AMOUNT).sort_index(ascending=False)

    # Fix month names
    df.index = [month_abbr[x] for x in df.index]

    cmap = {c.names.INCOMES: "Greens", c.names.EXPENSES: "YlOrRd"}[type_trans]

    data = go.Heatmap(
        x=df.columns, y=df.index, z=df.values, colorscale=cmap, reversescale=True, showscale=False
    )

    layout = go.Layout(title="Heatmap ({})".format(type_trans))
    return go.Figure(data=[data], layout=layout)


def dist_plot(dfg):
    """
        Creates a distribution plot with expenses, incomes and ebit

        Args:
            dfg:    dataframe to use

        Returns:
            the plotly plot as html-div format
    """

    dfe = u.group_df_by(dfg[dfg[c.cols.TYPE] == c.names.EXPENSES], "M")
    dfi = u.group_df_by(dfg[dfg[c.cols.TYPE] == c.names.INCOMES], "M")

    df_baii = dfi - dfe

    iter_data = [
        (df_baii, c.names.EBIT, c.colors.EBIT),
        (dfe, c.names.EXPENSES, c.colors.EXPENSES),
        (dfi, c.names.INCOMES, c.colors.INCOMES),
    ]

    # Generate traces to show. This allow to disable traces if there is no data
    data, names, colors = [], [], []
    for df, name, color in iter_data:

        # Some data needed
        if (df[c.cols.AMOUNT].sum() > 0) and (len(df[c.cols.AMOUNT].unique()) > 1):
            data.append(df[c.cols.AMOUNT].fillna(0).tolist())
            names.append(name)
            colors.append(color)

    if not data:
        return {}

    fig = FF.create_distplot(data, names, colors=colors, bin_size=100)

    fig["layout"].update(title="Incomes, Expenses and EBIT distribution")

    return fig
