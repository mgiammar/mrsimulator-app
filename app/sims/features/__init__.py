# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .fields import features_modal
from .fields import fields
from .fit_modal import fit_info_modal
from app.custom_widgets import custom_button


store = [
    # JSON string of Parameters object
    dcc.Store(id="params-data", storage_type="memory"),
    # Timestamps for triggering fitting callbacks
    dcc.Store(id="trigger-sim", storage_type="memory"),
    dcc.Store(id="trigger-fit", storage_type="memory"),
    dcc.Store(id="trigger-params-update", storage_type="memory"),
    # String for deciding which workflow to run
    dcc.Store(id="which-workflow", storage_type="memory"),
    # # Bool for choosing to update tables to new values
    # dcc.Store(id="update-vals", storage_type="memory"),
    # # Bool for triggering table update only after fit
    # dcc.Store(id="anticipate-table-update", storage_type="memory", data=False),
]
storage_div = html.Div(id="fitting-store", children=store)


def buttons():
    """Static user interface buttons"""
    kwargs = {"outline": True, "color": "dark", "size": "md"}
    simulate = custom_button(
        id="sim-button",
        icon_classname="far fa-chart-bar",
        tooltip="Simulate a spectrum using the current values.",
        **kwargs,
    )
    fit = custom_button(
        id="fit-button",
        icon_classname="fas fa-compress-alt",
        tooltip="Run least-squares minimization.",
        **kwargs,
    )
    return dbc.ButtonGroup([simulate, fit])


def feature_select():
    """Radio buttons for selecting spin system and method tables"""
    sys_select_buttons = dbc.RadioItems(
        id="sys-feature-select",
        className="table-select btn-group",
        labelClassName="btn btn-primary",
        labelCheckedClassName="active",
        labelStyle={"display": "inline-block"},
    )
    mth_select_buttons = dbc.RadioItems(
        id="mth-feature-select",
        className="table-select btn-group",
        labelClassName="btn btn-primary",
        labelCheckedClassName="active",
        labelStyle={"display": "inline-block"},
    )

    sys_head = html.Div(
        [html.H6("Spin Systems"), sys_select_buttons], className="feature-select"
    )
    mth_head = html.Div(
        [html.H6("Methods"), mth_select_buttons], className="feature-select"
    )
    return html.Div([sys_head, mth_head], id="feature-select-div")


def features_header():
    """Header for features tab"""
    help_button = html.Div(
        html.I(className="fas fa-question-circle pl-1 fa-lg"),
        id="fit-info-modal-button",
        style={"cursor": "pointer"},
    )
    icon = html.I(className="fas fa-bullseye fa-lg")
    text = html.H4("Features", className="hide-label-sm")
    title = html.Div([icon, text, help_button])
    return html.Div([title, buttons()], className="card-header")


def ui():
    page = html.Div(
        [
            features_header(),
            feature_select(),
            fields,
            fit_info_modal,
            features_modal,
            storage_div,
        ]
    )
    return html.Div(className="left-card", children=page, id="features-body")


features_body = ui()
