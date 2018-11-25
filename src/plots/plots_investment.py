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


def total_worth_plot(df_liq_in, df_wor_in, avg_month):
    """
        Creates a plot with investment and liquid

        Args:
            df_liq_in:  dataframe with liquid
            df_wor_in:  dataframe with investment worth
            avg_month:  month to use in rolling average

        Returns:
            the plotly plot as html-div format
    """

    df_liq = df_liq_in.set_index(c.cols.DATE)[[c.names.TOTAL]]
    df_wor = df_wor_in.set_index(c.cols.DATE)[[c.names.TOTAL]]

    df_liq = df_liq.rolling(avg_month, min_periods=1).mean().apply(lambda x: round(x, 2))
    df_wor = df_wor.rolling(avg_month, min_periods=1).mean().apply(lambda x: round(x, 2))

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