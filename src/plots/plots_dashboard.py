"""
	Individual plots
"""

from datetime import date, timedelta

import dash_html_components as html

import constants as c
from app import ui_utils as uiu


ARROWS = {True: "▲", False: "▼"}


def _get_stats(dfs, date_in):
    """
        Gets stats from old month

        Args:
            dfs:        dict with all dataframs
            date_in:    month of which stats are wanted
    """

    mdate = date_in.strftime("%Y-%m-01")

    dft = dfs[c.dfs.TRANS].copy()
    df = dft[dft[c.cols.MONTH_DATE] == mdate]

    out = {
        c.names.EXPENSES: df[df[c.cols.TYPE] == c.names.EXPENSES][c.cols.AMOUNT].sum(),
        c.names.INCOMES: df[df[c.cols.TYPE] == c.names.INCOMES][c.cols.AMOUNT].sum()
    }

    out[c.names.EBIT] = out[c.names.INCOMES] - out[c.names.EXPENSES]

    dfl = dfs[c.dfs.LIQUID].copy()
    # df_liquid has all months and ordered, we can call it directly
    out[c.names.LIQUID] = dfl.loc[dfl[c.cols.DATE] == mdate, c.names.TOTAL].tolist()[0]

    return out

def get_titles(dfs):
    """ Gets a list of h6 with data from previous month """

    mdate = date.today()
    date_m1 = (mdate.replace(day=1) - timedelta(days=1))
    date_m2 = (date_m1.replace(day=1) - timedelta(days=1))

    stats = _get_stats(dfs, date_m1)
    stats2 = _get_stats(dfs, date_m2)

    data = [
        uiu.get_one_column(
            html.H6("Stats for months {:%Y/%m} ({:%Y/%m})".format(date_m1, date_m2)),
            n_rows=4
        )
    ]

    for name, color in c.colors.COLORS.items():
        # bool stating if it is better than previous month (expenses should be reversed)
        aux = stats[name] > stats2[name]
        symbols = ARROWS[not aux if name == c.names.EXPENSES else aux]
        text = "{}: {:,.0f}€ ({:,.0f}€) {}".format(name, stats[name], stats2[name], symbols)

        # space as thousand separator
        text = text.replace(",", ".")

        data.append(
            uiu.get_one_column(
                html.H6(text, style={"color": color}),
                n_rows=2
            )
        )

    return data
