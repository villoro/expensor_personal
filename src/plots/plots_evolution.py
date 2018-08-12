"""
	Individual plots
"""

import plotly.graph_objs as go

import constants as c
import utilities as u


def plot_timeserie(dfg, timewindow="M"):
    """
        Creates a timeseries plot with expenses, incomes and their regressions

        Args:
            dfg:        dataframe with info
            timewindow: temporal grouping

        Returns:
            the plotly plot as html-div format
    """

    # Income/Expense traces
    iter_data = {c.names.INCOMES: c.colors.INCOMES, c.names.EXPENSES: c.colors.EXPENSES}

    data = []

    for name, color in iter_data.items():
        df = u.dfs.group_df_by(dfg[dfg[c.cols.TYPE] == name], timewindow)
        data.append(
            go.Scatter(
                x=df.index, y=df[c.cols.AMOUNT],
                marker={"color": color},
                name=name, mode="lines"
            )
        )

    # Calculate EBIT
    df = dfg.copy()
    mfilter = df[c.cols.TYPE] == c.names.EXPENSES
    df.loc[mfilter, c.cols.AMOUNT] = - df.loc[mfilter, c.cols.AMOUNT]

    # EBIT trace
    df = u.dfs.group_df_by(df, timewindow)
    data.append(
        go.Scatter(
            x=df.index, y=df[c.cols.AMOUNT],
            marker={"color": c.colors.EBIT},
            name=c.names.EBIT, mode="lines"
        )
    )

    layout = go.Layout(title="Evolution")
    return go.Figure(data=data, layout=layout)


def plot_timeserie_by_categories(dfg, df_categ, type_trans=c.names.EXPENSES, timewindow="M"):
    """
        Creates a timeseries plot detailed by category

        Args:
            dfg:        dataframe with info
            df_categ:   categories dataframe
            type_trans: type of transaction [Income/Expense]
            timewindow: temporal grouping

        Returns:
            the plotly plot as html-div format
    """

    df = dfg[dfg[c.cols.TYPE] == type_trans].copy()
    df_cat = df_categ[df_categ[c.cols.TYPE] == type_trans].set_index(c.cols.NAME)

    df_aux = u.dfs.group_df_by(df, timewindow)
    data = [go.Scatter(x=df_aux.index, y=df_aux[c.cols.AMOUNT],
                       marker={"color": "black"}, name=c.names.TOTAL)]

    for cat in df_cat.index:
        if cat in df_cat.index:
            color_index = df_cat.at[cat, c.cols.COLOR_INDEX]
            color_name = df_cat.at[cat, c.cols.COLOR_NAME]
            color = u.get_colors((color_name, color_index))
        else:
            color = u.get_colors(("black", 500))

        df_aux = u.dfs.group_df_by(df[df[c.cols.CATEGORY] == cat], timewindow)
        data.append(go.Bar(
            x=df_aux.index, y=df_aux[c.cols.AMOUNT],
            marker={"color": color}, name=cat
        ))

    layout = go.Layout(title="Evolution by category", barmode='stack')
    return go.Figure(data=data, layout=layout)
