from typing import Dict, Any
import pandas as pd
import numpy as np

import dash_bootstrap_components as dbc
import plotly.express as px
from math import floor
import json
import dash
from dash import Dash, dcc, html, Input, Output, State
from generate_graphs import *
from SettingsCard import card_layout

# https://www.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page Neighb maps
# https://capitalplanning.nyc.gov/capitalproject/846P-5FRESHN#12.88/40.5704/-74.1954 POI locations
# TODO Select price range of hotels (histogram) limit map view to those hotels
# TODO Limit results to distance from park for example


# df_clean = pd.read_csv("AirbnbWithDistances.csv", low_memory=False, index_col=0)

neighb = json.load(open("neighb.json"))
df_clean = pd.read_csv("AirbnbWithDistances.csv", index_col=0, low_memory=False)
df_neighbreviewmean = pd.read_csv("neighb_means.csv", low_memory=False)

df_clean.dropna(subset=["Number of Reviews"], inplace=True)
# df_clean["number of reviews"] = df_clean["Number of Reviews"] * 100

filter_val = "Price"
# min_val = min(df_clean["price"])
# max_val = max(df_clean["price"])


px.set_mapbox_access_token("pk.eyJ1IjoicG5pZXJvcCIsImEiOiJjbGFxdnJkNGMwMGtuM3FwYmN5czV5NnowIn0.mYk_lZjfdsJQhxbTBsRbmw")

# fig2 = generate_choropleth(frame=df_neighbreviewmean, poly_data=neighb, color_var="Review Score")
# fig_scat = generate_scatter(frame=df_clean, xval="distanceTimeSquare", yval="Price")

app = dash.Dash(eager_loading=True, external_stylesheets=[dbc.themes.CYBORG])
# https://bootswatch.com/cyborg/

app.layout = html.Div(className='page', children=[
    dbc.Row([
        dbc.Col(
            html.Div(children=[html.H1("Dashboard Prototype", style=dict(width='100%'), id="title_field")]),
            width="auto")
    ], justify="center"),
    dbc.Row([
        dbc.Col([html.Div(children=[
            dcc.Graph(id="scatter_map", style={'display': 'inline-block'}),
            dcc.Store(id="fig_store")])], width="auto"),
        dbc.Col([dcc.Graph(id="ch_graph", style={'display': 'inline-block'})], width="auto"),
        dbc.Col(card_layout)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(children=[
                dcc.RangeSlider(min(df_clean["Price"]), max(df_clean["Price"]), id="slider"),
                dcc.Graph(id="histogram")
            ]
            )
        ])
    ])
])


# Settings Id's
# swatch
# map_Color
# map_Size
# map_Scale
# chloro_Color
# hist_Var
# hist_Bins
# slider


@app.callback(
    [Output("histogram", "figure"),
    Output("scatter_map", "figure"),
    Output("ch_graph", "figure"),
    Output("slider", "min"),
    Output("slider", "max")],
    [Input("slider", "value"),
    Input("swatch", "value"),
    Input("map_Color", "value"),
    Input("map_Size", "value"),
    Input("map_Scale", "value"),
    Input("chloro_Color", "value"),
    Input("hist_Var", "value"),
    Input("hist_Bins", "value"),
    Input("slider_Var", "value")])
def update_graphs(slider_tuple, swatch, map_Color, map_Size, map_Scale, chloro_Color, hist_Var, hist_Bins, slider_var):
    map_Scale = int(map_Scale)
    hist_Bins = int(hist_Bins)
    if slider_tuple is not None:
        frame_subset = df_clean[(df_clean[slider_var] >= slider_tuple[0]) & (df_clean[slider_var] <= slider_tuple[1])]
    else:
        frame_subset = df_clean
    # histogram
    fig_hist = generate_hist(frame=frame_subset, x_val=hist_Var, bins=hist_Bins)
    #Scatter MapBox
    fig_scatter = generate_scattermap(frame=frame_subset, size_var=map_Size, color_var=map_Color,swatch=swatch, scale=map_Scale)
    #Chloro
    fig_chloro = generate_choropleth(frame= frame_subset, poly_data=neighb, color_var=chloro_Color, swatch=swatch)
    #slider
    slider_max = max(df_clean[slider_var])
    slider_min = min(df_clean[slider_var])
    return fig_hist, fig_scatter, fig_chloro, slider_min, slider_max
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == "__main__":
    app.run_server(debug=True)

# TODO Add support for multiple screen sizes
