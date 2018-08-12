"""
	Individual plots
"""

from datetime import date, timedelta

import dash_html_components as html

import constants as c
from utilities.io import get_money_lover_filename


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

    margin_h = 30

    # Header of the summary
    text = "Stats for months {:%Y/%m} ({:%Y/%m})".format(date_m1, date_m2)
    style = {"text-align": "left"}
    style.update(c.styles.get_style_wraper(margin_h, 40))
    data = [html.H4(text, style=style)]

    # Fill the summary with relevant stats
    for name, color in c.colors.COLORS.items():
        # bool stating if it is better than previous month (expenses should be reversed)
        aux = stats[name] > stats2[name]
        symbols = ARROWS[not aux if name == c.names.EXPENSES else aux]
        text = "{}: {:,.0f}€ ({:,.0f}€) {}".format(name, stats[name], stats2[name], symbols)

        # space as thousand separator
        text = text.replace(",", ".")
        style = {"color": color, "text-align": "left"}
        style.update(c.styles.get_style_wraper(margin_h, 10))

        data.append(html.H5(text, style=style))

    # Show a text with transactions excel file date
    name = get_money_lover_filename()
    text = "* Using data from {}".format(name.split(".")[0].replace("-", "/"))
    style = {"text-align": "left"}
    style.update(c.styles.get_style_wraper(margin_h, 40))
    data.append(html.Div(text, style=style))

    return data
