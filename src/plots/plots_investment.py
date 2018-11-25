"""
	Individual plots
"""

import plotly.graph_objs as go

import utilities as u
import constants as c

def invest_evolution_plot(df_in, avg_month):
    """
        Creates a plot for the investment evolution

        Args:
            df_in:      dataframe to plot
            avg_month:  month to use in rolling average

        Returns:
            the plotly plot as html-div format
    """

    df = df_in.set_index(c.cols.DATE)

    df = df.rolling(avg_month, min_periods=1).mean().apply(lambda x: round(x, 2))

    data = [go.Scatter(x=df.index, y=df[c.names.TOTAL],
                       marker={"color": "black"}, name=c.names.TOTAL)]

    for col in df.columns:
        if col != c.names.TOTAL:
            data.append(go.Bar(x=df.index, y=df[col], name=col))

    layout = go.Layout(title="Investment evolution", barmode="stack")
    return go.Figure(data=data, layout=layout)


def invest_evolution_plot(df_liq_in, df_inv_in, avg_month):
    """
        Creates a plot with investment and liquid

        Args:
            df_liq_in:  dataframe with liquid
            df_inv_in:  dataframe with investment worth
            avg_month:  month to use in rolling average

        Returns:
            the plotly plot as html-div format
    """

    df_liq = df_liq_in.set_index(c.cols.DATE)[[c.names.TOTAL]]
    df_inv = df_inv_in.set_index(c.cols.DATE)[[c.names.TOTAL]]

    df_liq = df_liq.rolling(avg_month, min_periods=1).mean().apply(lambda x: round(x, 2))
    df_inv = df_inv.rolling(avg_month, min_periods=1).mean().apply(lambda x: round(x, 2))

    data = [
        go.Bar(x=df_liq.index, y=df_liq[c.names.TOTAL],
               marker={"color": c.colors.LIQUID}, name=c.names.LIQUID),
        go.Bar(x=df_inv.index, y=df_inv[c.names.TOTAL],
               marker={"color": c.colors.WORTH}, name=c.names.WORTH),
    ]