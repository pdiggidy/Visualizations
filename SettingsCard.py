import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import Dash, dcc, html, Input, Output

card_layout = dbc.Card([
    dbc.CardBody([
        html.H4("Settings"),
        dbc.Row([
            dbc.Col(
                html.H5("Color Swatch"), width="auto"),
            dbc.Col(dbc.DropdownMenu(label="Menu"), width="auto")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(
                html.H5("Map Color Variable"), width="auto"),
            dbc.Col(dbc.DropdownMenu(label="Menu"), width="auto")
            ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H5("Map Size Variable"), width="auto"),
            dbc.Col(dbc.DropdownMenu(label="Menu"), width="auto")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H5("Histogram Variable"), width="auto"),
            dbc.Col(dbc.DropdownMenu(label="Menu"), width="auto")
        ], align="center", justify="between"),
        dbc.Row([
            dbc.Col(html.H5("Histogram Bins"), width="auto"),
            dbc.Col(dbc.Input(placeholder="50"), width="auto")
        ], align="center", justify="between")
    ])
])

# TODO Validate Input box
# TODO add classes and id's to all the input methods