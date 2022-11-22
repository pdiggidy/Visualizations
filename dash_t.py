from typing import Dict, Any
import pandas as pd
import numpy as np

from main import df_clean
import plotly.express as px
from math import floor
import json
from dash import html
from dash import dcc


import dash
neighb = json.load(open("neighb.json"))

df_clean["scaled"] = df_clean["review rate number"]
mean = floor(df_clean["scaled"].mean())
df_clean["scaled"].fillna(mean, inplace=True)
df_clean.dropna(subset=["number of reviews"], inplace=True)
df_clean["number of reviews"] = df_clean["number of reviews"]*100
#
df_test = df_clean.head(500)
px.set_mapbox_access_token("pk.eyJ1IjoicG5pZXJvcCIsImEiOiJjbGFxdnJkNGMwMGtuM3FwYmN5czV5NnowIn0.mYk_lZjfdsJQhxbTBsRbmw")
fig = px.scatter_mapbox(df_test, lat="lat", lon="long",color="scaled", size="number of reviews", color_continuous_scale="aggrnyl_r")
fig.update_traces(cluster=dict(enabled=True))
# fig.show()

fig = px.choropleth_mapbox(df_clean, geojson=neighb, locations="neighbourhood", featureidkey="properties.neighborhood",
                           color="scaled", center={"lat": 40.7128, "lon": -74.0060}, zoom=10, color_continuous_scale="aggrnyl_r")
fig.update_geos(fitbounds="locations", visible=False)

app=dash.Dash()

app.layout = html.Div(className='row', children=[
    html.H1("Tips database analysis (First dashboard)"),
    dcc.Dropdown(),
    html.Div(children=[
        dcc.Graph(id="graph1",figure=px.choropleth_mapbox(df_clean, geojson=neighb, locations="neighbourhood", featureidkey="properties.neighborhood",
                           color="scaled", center={"lat": 40.7128, "lon": -74.0060}, zoom=10, color_continuous_scale="aggrnyl_r"), style={'display': 'inline-block'})
    ])
])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == "__main__":
    app.run_server()