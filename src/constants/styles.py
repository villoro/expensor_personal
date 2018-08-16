"""
    Styles for dash
"""

from utilities.upalette import get_colors


HEIGHT_HEADER = 75
HEIGHT_FILTERS = 0
WIDTH_SIDEBAR = 300
PADDING_V = 10
PADDING_H = 15

COLOR_HEADER = get_colors(("blue", 500))
COLOR_SIDEBAR, COLOR_SIDEBAR_SEP = get_colors([("grey", 200), ("grey", 400)])

HEADER = {
    "background-color": COLOR_HEADER,
    "top": 0,
    "left": 0,
    "height": "{}px".format(HEIGHT_HEADER - PADDING_V),
    "width": "100%",
    "position": "fixed",
    "overflow": "hidden",
    "margin": "0px",
    "padding-top": "{}px".format(PADDING_V),
    "padding-left": "{}px".format(PADDING_H),
    "z-index": "9999"
}

SYNC_BUTTON = {
    "background-color": "white",
    "border-color": "white",
    "position": "absolute",
    "top": "50%",
    "transform": "translateY(-50%)",
}

SIDEBAR = {
    "background-color": COLOR_SIDEBAR,
    "top": HEIGHT_HEADER,
    "left": 0,
    "height": "100%",
    "width": "{}px".format(WIDTH_SIDEBAR - 2*PADDING_H),
    "position": "fixed",
    "overflow": "hidden",
    "padding-top": "{}px".format(PADDING_V),
    "padding-bottom": "{}px".format(PADDING_V),
    "padding-left": "{}px".format(PADDING_H),
    "padding-right": "{}px".format(PADDING_H),
}

FILTER_DIV = {
    "top": HEIGHT_HEADER,
    "left": WIDTH_SIDEBAR,
    "height": "{}px".format(HEIGHT_FILTERS),
    "width": "100%",
    "position": "fixed",
    "overflow": "hidden",
}

BODY = {
    "top": HEIGHT_HEADER + HEIGHT_FILTERS,
    "left": WIDTH_SIDEBAR,
    "right": 0,
    "bottom": 0,
    "position": "fixed",
    "padding": 0,
    "overflow-y": "scroll"
}

SIDEBAR_ELEM = {
    "padding-bottom": "25px",
    "border-bottom": "1px solid {}".format(COLOR_SIDEBAR_SEP)
}

DIV_CONTROL_IN_BODY = {
    "text-align": "center",
    "padding-bottom": "15px",
    "border-bottom": "2px solid {}".format(COLOR_SIDEBAR)
}

UPLOAD_CONTAINER = {
    "height": "60px",
    "lineHeight": "60px",
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "borderRadius": "5px",
    "textAlign": "center",
    "margin-top": "{}px".format(PADDING_V),
    "margin-left": "{}px".format(PADDING_H),
    "margin-right": "{}px".format(PADDING_H),
}

UPLOAD_INFO = {
    "text-align": "left",
    "margin-left": "{}px".format(20),
    "margin-right": "{}px".format(20),
}

HIDDEN = {"display": "none"}


def get_style_wraper(margin_h=10, margin_v=10):
    """
        Gets a style dict with margins
    """

    return {
        "margin-top": "{}px".format(margin_v),
        "margin-bottom": "{}px".format(margin_v),
        "margin-left": "{}px".format(margin_h),
        "margin-right": "{}px".format(margin_h),
    }
