"""
	Individual plots
"""

from datetime import date, timedelta

import dash_bootstrap_components as dbc
import dash_html_components as html

import constants as c
import layout as lay
from data_loader import get_money_lover_filename


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


def get_summary(dfs):
    """ Gets a list of h6 with data from previous month """

    mdate = date.today()
    date_m1 = (mdate.replace(day=1) - timedelta(days=1))
    date_m2 = (date_m1.replace(day=1) - timedelta(days=1))

    # Get stats for last month and the month previous to the last one
    stats = _get_stats(dfs, date_m1)
    stats2 = _get_stats(dfs, date_m2)


    # Header of the summary
    data = [["Stats for months", "{:%Y/%m} ({:%Y/%m})".format(date_m1, date_m2), "secundary"]]

    # Fill the summary with relevant stats
    for name, color in c.colors.COLORS_CARDS.items():
        # bool stating if it is better than previous month (expenses should be reversed)
        aux = stats[name] > stats2[name]
        symbols = ARROWS[not aux if name == c.names.EXPENSES else aux]

        # space as thousand separator
        text = f"{stats[name]:,.0f}€ ({stats2[name]:,.0f}€) {symbols}".replace(",", ".")

        data.append([name, text, color])


    # Show a text with transactions excel file date
    data.append(["Using data from", name.split(".")[0].replace("-", "/"), "secundary"])

    return dbc.CardDeck(
        [
            dbc.Card(
                [
                    dbc.CardTitle(title),
                    dbc.CardText(text)
                ],
                color=color,
                className="w3-center",
                style=lay.padding()
            ) for title, text, color in data
        ],
        style=lay.padding(),
    )
