# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app import app

__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


def add_title():
    """Static title for add node modal"""
    return dbc.ModalHeader("Add Node")


def add_body():
    """Static body for add node modal"""
    # Inputs and messages here
    modal_text = html.Div("Enter a new node name and click enter")
    node_name = dbc.Input(id="new-node-name", type="text")
    return dbc.ModalBody([modal_text, node_name])


def add_footer():
    """Static footer for add node modal"""
    submit = dbc.Button(id="add-node-submit-button", children="Submit")
    cancel = dbc.Button(id="add-node-cancel-button", children="Cancel")

    return dbc.ModalFooter([submit, cancel])


def add_ui():
    """Static add node modal"""
    return dbc.Modal(
        children=[add_title(), add_body(), add_footer()],
        id="add-node-modal",
        is_open=False,
        # addtl args here
    )


add_node_modal = add_ui()


def node_title(name):
    """Dynamic node modal title"""
    return dbc.ModalHeader(f"Node: {name}")


def node_body(name, data, *args):
    """Dynamic node modal body displaying node info

    Params:
        name: name of clicked node
        data: `couplings-data`
        args: data to be displayed
    """
    # Add more info as couplings develop
    add_coupling_dropdown = html.Div(
        dcc.Dropdown(id="new-coupling-dropdown", options=data_to_dropdown(name, data))
    )
    coupling_strength = html.Div(
        dbc.Input(id="new-coupling-strength", type="number")
    )  # Update type for proper formatting
    return dbc.ModalBody(
        id="node-modal-body", children=[add_coupling_dropdown, coupling_strength]
    )


def node_footer():
    """Modal footer buttons"""
    submit_button = html.Button(id="node-modal-submit-button", children="Submit")
    delete_button = html.Button(id="node-modal-delete-button", children="Delete")
    close_button = html.Button(id="node-modal-close-button", children="Close")
    return dbc.ModalFooter([submit_button, delete_button, close_button])


def data_to_dropdown(name, data):
    """Constructs list of dicts for dcc.Dropdown component

    Params:
        name: selection to be excluded
        data: sotred Cytoscape relation data
    """
    options = []
    if name == "" and data is None:
        return options
    # Need to split data into nodes and edges before comprehensions
    data = [node["data"] for node in data]
    # print(name)
    # print(data)

    # Clean up into list/dict comp OR modify `data` and return
    for node in data:
        if name != node["label"]:
            _dict = {}
            _dict["label"] = node["label"]
            _dict["value"] = node["id"]
            options.append(_dict)

    return options


def node_ui():
    """Dynamic node info modal"""
    # modal = dbc.Modal(id="node-modal", children=[node_title(""), node_body("", None), node_footer()])
    modal = dbc.Modal(
        id="node-modal", children=[node_footer(), node_body("", None), node_footer()]
    )
    return modal


node_modal = node_ui()


# Callbacks ============================================================================
# app.clientside_callback(
#     "function(n1, n2, n3, is_open) { return !is_open; }",
#     Output("add-node-modal", "is_open"),

#     Input("add-node-button", "n_clicks"),
#     Input("add-node-submit-button", "n_clicks"),
#     Input("add-node-cancel-button", "n_clicks"),

#     State("add-node-modal", "is_open"),
#     prevent_initial_call=True
# )
# BUG: clientside_callback not working even though exact same code as other modals


@app.callback(
    Output("add-node-modal", "is_open"),
    Input("add-node-button", "n_clicks"),
    Input("add-node-submit-button", "n_clicks"),
    Input("add-node-cancel-button", "n_clicks"),
    State("add-node-modal", "is_open"),
    prevent_initial_call=True,
)
def open_add_node_modal(n1, n2, n3, is_open):
    """Opens/Closes add node modal"""
    return not is_open


@app.callback(
    Output("node-modal", "children"),
    Output("node-modal", "is_open"),
    Input(
        "couplings-cyto", "tapNodeData"
    ),  # NOTE: Does not trigger on same node tapped twice
    Input("node-modal-submit-button", "n_clicks"),
    Input("node-modal-delete-button", "n_clicks"),
    Input("node-modal-close-button", "n_clicks"),
    State("couplings-data", "data"),
    prevent_initial_call=True,
)
def open_node_info_modal(tap, n1, n2, n3, coup_data):
    """Creates and opens or closes the node info modal"""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    print("node info", trigger_id)

    return CALLBACKS[trigger_id]()


def make_and_open_modal():
    """Updates modal childeren and opens"""
    tap_data = ctx.inputs["couplings-cyto.tapNodeData"]
    data = ctx.states["couplings-data.data"]

    title = node_title(tap_data["label"])
    body = node_body(tap_data["label"], data)
    children = children = [title, body, node_footer()]

    return children, True


def close_node_modal():
    """Close node modal"""
    return no_update, False


CALLBACKS = {
    "couplings-cyto": make_and_open_modal,
    "node-modal-submit-button": close_node_modal,
    "node-modal-close-button": close_node_modal,
    "node-modal-delete-button": close_node_modal,
}


# Tap edge callback
