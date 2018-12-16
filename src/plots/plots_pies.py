"""
	Individual plots
"""

import plotly.graph_objs as go

import utilities as u
import constants as c


def get_pie(dfg, df_categ, type_trans, years=None, height=None):
    """
        Creates a pie with expenses or incomes

        Args:
            dfg:        dataframe to use
            df_categ:   categories dataframe
            type_trans: type of transaction [Income/Expense]
            years:      years to include in the plot
            height:     allow custom height of the plot

        Returns:
            the plotly plot as html-div format
    """

    df = u.dfs.filter_data(dfg, years, c.cols.YEAR)
    df = df[df[c.cols.TYPE] == type_trans]
    df_cat = df_categ[df_categ[c.cols.TYPE] == type_trans].set_index(c.cols.NAME)

    df = df.groupby(c.cols.CATEGORY).sum()

    # Order using order from categories dataframe
    df = df.reindex(df_cat.index)

    colors = []
    for x in df.index:
        if x in df_cat.index:
            color_index = df_cat.at[x, c.cols.COLOR_INDEX]
            color_name = df_cat.at[x, c.cols.COLOR_NAME]
            colors.append(u.get_colors((color_name, color_index)))
        else:
            colors.append(u.get_colors(("black", 500)))

    data = go.Pie(values=df[c.cols.AMOUNT], labels=df.index, marker={"colors": colors}, sort=False)

    layout = go.Layout(title="{} distribution".format(type_trans))

    if height:
        layout.update({"height": height})

    return go.Figure(data=[data], layout=layout)
