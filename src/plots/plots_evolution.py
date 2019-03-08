"""
    Individual plots
"""

import pandas as pd
import plotly.graph_objs as go

import constants as c
import utilities as u


def plot_timeserie(dfg, avg_month, timewindow="M", height=None):
    """
        Creates a timeseries plot with expenses, incomes and their regressions

        Args:
            dfg:        dataframe with info
            avg_month:  month to use in time average
            timewindow: temporal grouping
            height:     height of the plot

        Returns:
            the plotly plot as html-div format
    """

    # Income/Expense traces
    iter_data = {c.names.INCOMES: c.colors.INCOMES, c.names.EXPENSES: c.colors.EXPENSES}

    data = []

    for name, color in iter_data.items():
        df = u.group_df_with_time_avg(dfg[dfg[c.cols.TYPE] == name], timewindow, avg_month)
        data.append(
            go.Scatter(
                x=df.index, y=df[c.cols.AMOUNT], marker={"color": color}, name=name, mode="lines"
            )
        )

    # EBIT trace
    df = u.group_df_with_time_avg(u.get_ebit(dfg), timewindow, avg_month)

    data.append(
        go.Scatter(
            x=df.index,
            y=df[c.cols.AMOUNT],
            marker={"color": c.colors.EBIT},
            name=c.names.EBIT,
            mode="lines",
        )
    )

    layout = go.Layout(title="Evolution", height=height)
    return go.Figure(data=data, layout=layout)


def plot_timeserie_by_categories(
    dfg, df_categ, avg_month, type_trans=c.names.EXPENSES, timewindow="M"
):
    """
        Creates a timeseries plot detailed by category

        Args:
            dfg:        dataframe with info
            df_categ:   categories dataframe
            avg_month:  month to use in time average
            type_trans: type of transaction [Income/Expense]
            timewindow: temporal grouping

        Returns:
            the plotly plot as html-div format
    """

    df = dfg[dfg[c.cols.TYPE] == type_trans].copy()
    df_cat = df_categ[df_categ[c.cols.TYPE] == type_trans].set_index(c.cols.NAME)

    df_aux = u.group_df_with_time_avg(df, timewindow, avg_month, dfg)

    data = [
        go.Scatter(
            x=df_aux.index, y=df_aux[c.cols.AMOUNT], marker={"color": "black"}, name=c.names.TOTAL
        )
    ]

    for cat in df_cat.index:
        if cat in df_cat.index:
            color_index = df_cat.at[cat, c.cols.COLOR_INDEX]
            color_name = df_cat.at[cat, c.cols.COLOR_NAME]
            color = u.get_colors((color_name, color_index))
        else:
            color = u.get_colors(("black", 500))

        df_aux = u.group_df_with_time_avg(
            df[df[c.cols.CATEGORY] == cat], timewindow, avg_month, dfg
        )
        data.append(
            go.Bar(x=df_aux.index, y=df_aux[c.cols.AMOUNT], marker={"color": color}, name=cat)
        )

    layout = go.Layout(title="Evolution by category", barmode="stack", height=600)
    return go.Figure(data=data, layout=layout)


def plot_savings_ratio(dfg, avg_month, timewindow="M"):
    """
        Plots the ratio between ebit and incomes

        Args:
            dfg:        dataframe with info
            avg_month:  month to use in time average
            timewindow: temporal grouping

        Returns:
            the plotly plot as html-div format
    """

    # Calculate EBIT
    df = u.group_df_with_time_avg(u.get_ebit(dfg), timewindow, avg_month)

    # Incomes
    dfi = u.group_df_with_time_avg(dfg[dfg[c.cols.TYPE] == c.names.INCOMES], timewindow, avg_month)

    # Savings ratio
    df = df[c.cols.AMOUNT] / dfi[c.cols.AMOUNT]

    # Only positive values
    df = df.apply(lambda x: 0 if pd.isnull(x) else max(0, x))

    data = [
        go.Scatter(
            x=df.index,
            y=df,
            marker={"color": c.colors.SAVINGS},
            name=c.names.SAVINGS_RATIO,
            mode="lines",
        )
    ]

    layout = go.Layout(title="Ratio savings/incomes")
    return go.Figure(data=data, layout=layout)
