"""
	Individual plots
"""

import plotly.graph_objs as go

import constants as c
import utilities as u
from data_loader import YML


def invest_evolution_plot(df_in, avg_month):
    """
        Creates a plot for the investment evolution

        Args:
            df_in:      dataframe to plot
            avg_month:  month to use in time average

        Returns:
            the plotly plot as html-div format
    """

    df = df_in.set_index(c.cols.DATE)

    df = u.dfs.time_average(df, avg_month)

    data = [go.Scatter(x=df.index, y=df[c.names.TOTAL],
                       marker={"color": "black"}, name=c.names.TOTAL)]

    # If config file use it
    if c.yml.INVEST in YML:
        for name, config in YML[c.yml.INVEST].items():

            # Check that accounts are in the config
            mlist = [x for x in config[c.yml.ACCOUNTS] if x in df.columns]

            df_aux = df[mlist].sum(axis=1)
            color = u.get_colors((config[c.yml.COLOR_NAME], config[c.yml.COLOR_INDEX]))

            data.append(go.Bar(x=df_aux.index, y=df_aux, marker={"color": color}, name=name))

    # If not, simply plot the present columns
    else:
        for col in df.columns:
            if col != c.names.TOTAL:
                data.append(go.Bar(x=df.index, y=df[col], name=col))

    layout = go.Layout(title="Investment evolution", barmode="stack")
    return go.Figure(data=data, layout=layout)


def total_worth_plot(df_liq_in, df_wor_in, avg_month):
    """
        Creates a plot with investment and liquid

        Args:
            df_liq_in:  dataframe with liquid
            df_wor_in:  dataframe with investment worth
            avg_month:  month to use in time average

        Returns:
            the plotly plot as html-div format
    """

    df_liq = df_liq_in.set_index(c.cols.DATE)[[c.names.TOTAL]]
    df_wor = df_wor_in.set_index(c.cols.DATE)[[c.names.TOTAL]]

    df_liq = u.dfs.time_average(df_liq, avg_month)
    df_wor = u.dfs.time_average(df_wor, avg_month)

    # If indexs have different lenghts, normalize them
    index = df_wor.index if df_wor.shape[0] > df_liq.shape[0] else df_liq.index
    df_liq = df_liq.reindex(index).fillna(0)
    df_wor = df_wor.reindex(index).fillna(0)

    dft = df_liq + df_wor

    data = [
        go.Bar(x=df_liq.index, y=df_liq[c.names.TOTAL],
               marker={"color": c.colors.LIQUID}, name=c.names.LIQUID),
        go.Bar(x=df_wor.index, y=df_wor[c.names.TOTAL],
               marker={"color": c.colors.WORTH}, name=c.names.WORTH),
        go.Scatter(x=dft.index, y=dft[c.names.TOTAL],
                   marker={"color": "black"}, name=c.names.TOTAL)
    ]

    layout = go.Layout(title="Total worth evolution", barmode="stack")
    return go.Figure(data=data, layout=layout)


def passive_income_vs_expenses(df_wor_in, df_trans_in, avg_month, smooth):
    """
        Compares what can be generated with passive income to expanses

        Args:
            df_wor_in:      dataframe with investment worth
            df_trans_in:    dataframe with transactions
            avg_month:      month to use in time average
            smooth:     bool to allow/disable passive smoothing

        Returns:
            the plotly plot as html-div format
    """

    dfw = df_wor_in.set_index(c.cols.DATE)[[c.names.TOTAL]]
    if smooth:
        dfw = u.dfs.time_average(dfw, avg_month)

    dfe = u.dfs.group_df_by(df_trans_in[df_trans_in[c.cols.TYPE] == c.names.EXPENSES], "M")
    dfe = u.dfs.time_average(dfe, avg_month)

    data = [
        go.Scatter(
            x=dfw.index, y=dfw[c.names.TOTAL]*0.04/12,
            name="Passive income", marker={"color": c.colors.INCOMES_PASSIVE}
        ),
        go.Scatter(
            x=dfe.index, y=dfe[c.cols.AMOUNT],
            name="Expenses", marker={"color": c.colors.EXPENSES}
        ),
    ]

    layout = go.Layout(title="Passive income vs expenses", barmode="stack")
    return go.Figure(data=data, layout=layout)
