# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .node_graph import node_graph

__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


store = [
    # list of dicts for Dash Cytoscape relations
    # Should this store `mrsimulator` couplings or `Cytoscape` info 
    dcc.Store(id="couplings-data", storage_type="memory", data=[]),  # Need to seralize into `local-mrsim-data`
    dcc.Store(id="trigger-couplings-update", storage_type="memory"),
    # addtl stores here
]
storage_div = html.Div(id="couplings-store", children=store)


def buttons():
    """Static user interface buttons for couplings graph"""
    # Add formatting after features implemented
    reset = html.Button(id="reset-couplings-button", children="reset")  # Temporary button for testing
    add_node = html.Button(id="add-node-button", children="Add Node")
    del_node = html.Button(id="del-node-button", children="Delete Node")
    submit_couplings = html.Button(id="submit-couplings-button", children="Submit")
    # More buttons here
    
    # Adjust return to button group
    return html.Div([reset, add_node, del_node, submit_couplings])


def couplings_header():
    """Static header for couplings interface"""
    # icon here
    text = html.H4("Couplings")

    title = html.Div(text)
    # Adjust return to element group eventually
    return html.Div([title, buttons()], className="card-header")


def ui():
    page = html.Div([couplings_header(), node_graph, storage_div])
    return html.Div(className="left-card", children=page, id="couplings-body")


couplings_body = ui()
