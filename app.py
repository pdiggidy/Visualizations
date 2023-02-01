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


df_clean = pd.read_csv("AirbnbClean.csv", low_memory=False, index_col=0)

neighb = json.load(open("neighb.json"))
df_clean = pd.read_csv("AirbnbClean.csv", index_col=0, low_memory=False)
df_neighbreviewmean = pd.read_csv("neighb_means.csv", low_memory=False)


df_clean.dropna(subset=["number of reviews"], inplace=True)
df_clean["number of reviews"] = df_clean["number of reviews"] * 100

filter_val = "price"
# min_val = min(df_clean["price"])
# max_val = max(df_clean["price"])


px.set_mapbox_access_token("pk.eyJ1IjoicG5pZXJvcCIsImEiOiJjbGFxdnJkNGMwMGtuM3FwYmN5czV5NnowIn0.mYk_lZjfdsJQhxbTBsRbmw")

fig2 = generate_choropleth(frame=df_neighbreviewmean, poly_data=neighb, color_var="review rate number")
fig_scat = generate_scatter(frame=df_clean, xval="distanceTimeSquare", yval="price")


app = dash.Dash(eager_loading=True, external_stylesheets=[dbc.themes.CYBORG])
#https://bootswatch.com/cyborg/

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
        dbc.Col([dcc.Graph(id="ch_graph", figure=fig2, style={'display': 'inline-block'})], width="auto"),
        dbc.Col(card_layout)
    ]),
    dbc.Row([
        dbc.Col([
                html.Div(children=[
                        dcc.RangeSlider(min(df_clean["price"]), max(df_clean["price"]), 100, id="slider"),
                        dcc.Graph(id="histogram")
                        ]
        )
    ])
        ])
    ])




@app.callback(
    Output("histogram", "figure"),
    Output("scatter_map", "figure"),
    Output("ch_graph", "figure"),
    Input("slider", "value"))
def update_graphs(val):
    if val:
        df_subset = df_clean[(df_clean[filter_val] >= val[0]) & (df_clean[filter_val] <= val[1])]
        fig_hist = generate_hist(df_subset, "price")  # , val[0], val[1])
        fig_scatter = generate_scattermap(df_subset, "price", "review rate number")
        fig_chlo = generate_choropleth(df_subset, poly_data=neighb, color_var="review rate number")

    else:
        fig_hist = generate_hist(df_clean, "price")
        fig_scatter = generate_scattermap(df_clean, "price", "review rate number")
        fig_chlo = generate_choropleth(df_clean, poly_data=neighb, color_var="review rate number")
    return fig_hist, fig_scatter, fig_chlo


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == "__main__":
    app.run_server(debug=True)


# TODO Add support for multiple screen sizes