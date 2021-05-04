# RENAME: use `node_graph` (avoid ambiguity) or just `graph`
# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app import app
from app.custom_widgets import custom_button
from .modal import add_node_modal
from .modal import node_modal

__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


def cyto_graph():
    """Dynamic user interface for spin systems and couplings"""
    _cyto = cyto.Cytoscape(
        id="couplings-cyto",
        layout={"name": "grid"},
        autoRefreshLayout=True,
        style={
            "width": "100%",
            "height": "500px",
        },  # Can this be replaced with CSS file
        elements=[],
    )
    return _cyto


def ui():
    """Couplings UI"""
    return html.Div(
        id="node_graph-ui", children=[cyto_graph(), add_node_modal, node_modal]
    )


node_graph = ui()


# Callbacks ============================================================================
@app.callback(
    Output("couplings-cyto", "elements"),
    Output("couplings-data", "data"),
    Input("reset-couplings-button", "n_clicks"),
    Input("add-node-submit-button", "n_clicks"),
    Input("node-modal-submit-button", "n_clicks"),
    Input("node-modal-delete-button", "n_clicks"),
    # Input("couplings-data", "data"),
    Input("trigger-couplings-update", "data"),
    State("local-mrsim-data", "data"),
    State("couplings-data", "data"),
    State("couplings-cyto", "tapNodeData"),
    State("new-node-name", "value"),
    State("new-coupling-dropdown", "value"),
    State("new-coupling-strength", "value"),
    prevent_initial_call=True,
)
def update_couplings(*args):
    """Updates coupling data and body"""
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("couplings data", trigger_id)

    return CALLBACKS[trigger_id]()


def reset_couplings():
    """Debugging button (to be removed)"""
    return [], []


def add_node():
    """Adds new node to graph from vals in modal"""
    data = ctx.states["couplings-data.data"]
    name = ctx.states["new-node-name.value"]

    # Check to not add same node-id

    data.append({"data": {"id": "node-" + name.replace(" ", "_"), "label": name}})
    return data, data


def del_node():
    """Deletes a node"""
    data = ctx.states["couplings-data.data"]
    tap_data = ctx.states["couplings-cyto.tapNodeData"]

    # Add safegaurds for errors
    # Need to delete edges as well?
    data.remove({"data": tap_data})

    return data, data


def add_edge():
    """Adds an edge (coupling) between two nodes"""
    data = ctx.states["couplings-data.data"]
    tap_data = ctx.states["couplings-cyto.tapNodeData"]
    target_node = ctx.states["new-coupling-dropdown.value"]
    strength = ctx.states["new-coupling-strength.value"]

    return no_update, no_update


def construct_couplings_graph():
    """Constructs couplings graph on `couplings-data` update"""
    mrsim_data = ctx.states["local-mrsim-data.data"]

    if "couplings" in mrsim_data:
        # parse or just grab
        cyto_data = mrsim_data["couplings"]
    else:
        cyto_data = []

    return cyto_data, cyto_data


def cyto_data_to_mrsim_couplings(data):
    """Convernt Cytoscape list into mrsimulator couplings (dic/list?)"""
    raise NotImplementedError


def mrsim_couplings_to_cyto_data(data):
    """Convernt mrsimulator couplings (dic/list?) into Cytoscape"""
    raise NotImplementedError


CALLBACKS = {
    "reset-couplings-button": reset_couplings,
    "add-node-submit-button": add_node,
    "node-modal-delete-button": del_node,
    "node-modal-submit-button": add_edge,
    # "couplings-data": construct_couplings_graph,
    "trigger-couplings-update": construct_couplings_graph,
}