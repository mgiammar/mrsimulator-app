# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .fields import fields
from .fit_modal import fit_info_modal
from app import app
from app.custom_widgets import custom_button


store = [
    # JSON string of Parameters object
    dcc.Store(id="params-data", storage_type="memory"),
    # Timestamps for triggering fitting callbacks
    dcc.Store(id="trigger-sim", storage_type="memory"),
    dcc.Store(id="trigger-fit", storage_type="memory"),
    dcc.Store(id="trigger-table-update", storage_type="memory"),
]
storage_div = html.Div(id="fitting-store", children=store)


def buttons():
    """Static user interface buttons"""
    kwargs = {"outline": True, "color": "dark", "size": "sm"}
    reset = custom_button(
        id="reset-button",
        text="Reset",
        tooltip="Reset the parameter to default values.",
        **kwargs
    )
    simulate = custom_button(
        id="simulate-button",
        text="Simulate",
        tooltip="Simulate a spectrum using the current values.",
        **kwargs
    )
    fit = custom_button(
        id="run-fitting-button",
        text="Fit",
        tooltip="Run least-squares minimization.",
        **kwargs
    )
    return dbc.ButtonGroup([reset, simulate, fit])


def fit_header():
    """Header for fitting tab"""
    help_button = html.Div(
        html.I(className="fas fa-question-circle pl-1 fa-lg"),
        id="fit-info-modal-button",
        style={"cursor": "pointer"},
    )
    icon = html.I(className="fas fa-bullseye fa-lg")
    text = html.H4("Fitting Parameters", className="hide-label-sm")
    title = html.Div([icon, text, help_button])
    return html.Div([title, buttons()], className="card-header")


def ui():
    page = html.Div([fit_header(), fields, fit_info_modal, storage_div])
    return html.Div(className="left-card", children=page, id="fit-body")


fit_body = ui()
