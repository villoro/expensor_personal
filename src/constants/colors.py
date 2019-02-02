"""
    Some colors
"""

from v_palette import get_colors

from constants import names


EXPENSES = get_colors(("red", 500))
INCOMES = get_colors(("green", 500))
INCOMES_PASSIVE = get_colors(("green", 700))
EBIT = get_colors(("amber", 500))
EBIT_CUM = get_colors(("blue", 500))
LIQUID = get_colors(("blue", 400))
LIQUID_MIN_REC = get_colors(("grey", 700))
LIQUID_REC = get_colors(("grey", 400))
WORTH = get_colors(("lime", 400))
SAVINGS = get_colors(("purple", 500))

TABLE_HEADER_FILL = get_colors(("blue", 200))

COLORS = {
    names.INCOMES: INCOMES,
    names.EXPENSES: EXPENSES,
    names.EBIT: EBIT,
    names.LIQUID: LIQUID
}

COLORS_CARDS = {
    names.INCOMES: "success",
    names.EXPENSES: "danger",
    names.EBIT: "warning",
    names.LIQUID: "primary"
}
