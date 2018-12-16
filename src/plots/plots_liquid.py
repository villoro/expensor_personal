"""
	Individual plots
"""

import plotly.graph_objs as go

import constants as c
import utilities as u


MONTHS_MIN = 3
MONTHS_REC = 6

def liquid_plot(df_liq_in, df_list, avg_month):
    """
        Creates a plot for the liquid evolution

        Args:
            df_liq_in:  dataframe with liquid info
            df_list:    dataframe with types of liquids
            avg_month:  month to use in time average

        Returns:
            the plotly plot as html-div format
    """

    df_liq = df_liq_in.set_index(c.cols.DATE)
    df_liq = u.dfs.time_average(df_liq.fillna(0), avg_month)

    data = [go.Scatter(x=df_liq.index, y=df_liq[c.names.TOTAL],
                       marker={"color": "black"}, name=c.names.TOTAL)]

    for level in df_list[c.cols.LIQUID_LEVEL].unique():
        df_aux = df_list[df_list[c.cols.LIQUID_LEVEL] == level]
        name_liq = df_aux[c.cols.LIQUID_NAME].tolist()[0]
        name_trace = "{} - {}".format(level, name_liq)

        df = df_liq[df_aux[c.cols.NAME].tolist()].sum(axis=1)
        color = u.get_colors(("blue", 100 + 200*level))

        data.append(go.Bar(x=df.index, y=df, marker={"color": color}, name=name_trace))

    layout = go.Layout(title="Liquid evolution", barmode="stack")
    return go.Figure(data=data, layout=layout)


def plot_expenses_vs_liquid(df_liquid_in, df_trans_in, avg_month, show_rec=True):
    """
        Creates a plot to compare liquid and expenses

        Args:
            df_liq_in:      dataframe with liquid info
            df_trans_in:    dataframe with transactions
            avg_month:      month to use in time average
            show_rec:       bool for show/hide recommended liquids

        Returns:
            the plotly plot as html-div format
    """

    df_l = df_liquid_in.set_index(c.cols.DATE).copy()
    df_l = u.dfs.time_average(df_l.fillna(0), avg_month)

    df_t = u.dfs.group_df_by(df_trans_in[df_trans_in[c.cols.TYPE] == c.names.EXPENSES], "M")
    df_t = u.dfs.time_average(df_t, avg_month)

    iter_data = [
        (df_t, df_t[c.cols.AMOUNT], c.names.EXPENSES, c.colors.EXPENSES),
        (df_l, df_l[c.names.TOTAL], c.names.LIQUID, c.colors.LIQUID),
        (df_t, MONTHS_MIN*df_t[c.cols.AMOUNT], c.names.LIQUID_MIN_REC, c.colors.LIQUID_MIN_REC),
        (df_t, MONTHS_REC*df_t[c.cols.AMOUNT], c.names.LIQUID_REC, c.colors.LIQUID_REC),
    ]

    if not show_rec:
        iter_data = iter_data[:2]

    data = [go.Scatter(x=df.index, y=y, name=name, marker={"color": color}, mode="lines")
            for df, y, name, color in iter_data]

    layout = go.Layout(title="Liquid vs Expenses", showlegend=show_rec)
    return go.Figure(data=data, layout=layout)


def plot_months(df_liquid_in, df_trans_in, avg_month, show_rec=True):
    """
        Creates a plot to compare liquid and expenses

        Args:
            df_liq_in:      dataframe with liquid info
            df_trans_in:    dataframe with transactions
            avg_month:      month to use in time average
            show_rec:       bool for show/hide recommended liquids

        Returns:
            the plotly plot as html-div format
    """

    df_l = df_liquid_in.set_index(c.cols.DATE).copy()
    df_l = u.dfs.time_average(df_l.fillna(0), avg_month)

    df_t = u.dfs.group_df_by(df_trans_in[df_trans_in[c.cols.TYPE] == c.names.EXPENSES], "M")
    df_t = u.dfs.time_average(df_t, avg_month)

    serie = df_l[c.names.TOTAL]/df_t[c.cols.AMOUNT]

    iter_data = [
        (serie, "Months", c.colors.LIQUID),
        ([MONTHS_MIN]*len(serie), "Minimum months of liquid", c.colors.LIQUID_MIN_REC),
        ([MONTHS_REC]*len(serie), "Recommended months of liquid", c.colors.LIQUID_REC),
    ]

    if not show_rec:
        iter_data = iter_data[:1]

    data = [go.Scatter(x=serie.index, y=y, name=name, marker={"color": color}, mode="lines")
            for y, name, color in iter_data]

    layout = go.Layout(title="Survival months with current liquid")
    return go.Figure(data=data, layout=layout)
