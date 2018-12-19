"""
    OS related constants
"""

LINK_ROOT = "http://localhost:8050"
LINK_ROOT_LOGIN = "http://{}:{}@localhost:8050"

LINK_MAIN = "/"
LINK_DASHBOARD = "/dash"
LINK_EVOLUTION = "/evolution"
LINK_COMPARISON = "/compare"
LINK_HEATMAPS = "/heatmaps"
LINK_PIES = "/pies"
LINK_LIQUID = "/liquid"
LINK_INVESTMENTS = "/invest"

LANDING_APP = LINK_DASHBOARD

NUM_DICT = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"
}

LINKS_ALL = [
    LINK_DASHBOARD, LINK_EVOLUTION, LINK_COMPARISON, LINK_PIES, LINK_HEATMAPS, LINK_LIQUID,
    LINK_INVESTMENTS
]

INPUT_CATEGORIES = "categories"
INPUT_SMOOTHING = "smoothing"
INPUT_TIMEWINDOW = "timewindow"

DEFAULT_SMOOTHING = 1

PLOT_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["sendDataToCloud", "select2d", "lasso2d", "resetScale2d"]
}
