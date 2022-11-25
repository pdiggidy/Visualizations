from typing import Dict, Any
import pandas as pd
import numpy as np

from clean import df_clean
import plotly.express as px
from math import floor
import json
from dash import Dash, dcc, html, Input, Output
from generate_graphs import generate_scatter, generate_choropleth

import dash

neighb = json.load(open("neighb.json"))

df_clean["scaled"] = df_clean["review rate number"]
mean = floor(df_clean["scaled"].mean())
df_clean["scaled"].fillna(mean, inplace=True)
df_clean.dropna(subset=["number of reviews"], inplace=True)
df_clean["number of reviews"] = df_clean["number of reviews"] * 100

df_test = df_clean
px.set_mapbox_access_token("pk.eyJ1IjoicG5pZXJvcCIsImEiOiJjbGFxdnJkNGMwMGtuM3FwYmN5czV5NnowIn0.mYk_lZjfdsJQhxbTBsRbmw")
fig = px.scatter_mapbox(df_test, lat="lat", lon="long", color="scaled", size="number of reviews",
                        color_continuous_scale="aggrnyl_r")
# fig.update_traces(cluster=dict(enabled=True, color=["blue","red","green"], maxzoom=11))
# fig.show()

fig2 = px.choropleth_mapbox(df_clean, geojson=neighb, locations="neighbourhood", featureidkey="properties.neighborhood",
                            color="scaled", center={"lat": 40.7128, "lon": -74.0060}, zoom=10,
                            color_continuous_scale="aggrnyl_r")
fig2.update_geos(fitbounds="locations", visible=False)

app = dash.Dash()

app.layout = html.Div(className='row', children=[
    html.H1("Dashboard Prototype"),
    dcc.Dropdown(["number of reviews", "Reviews per month"], value="number of reviews", id="drop"),
    html.Div(children=[
        dcc.Graph(id="graph1", figure=fig, style={'display': 'inline-block'}),
        dcc.Graph(id="ch_graph", figure=fig2, style={'display': 'inline-block'})
    ])
])


@app.callback(Output(component_id="graph1", component_property="figure"), Input("drop", "value"))
def update_graphs(input_value):
    return generate_scatter(frame=df_clean,color_var=input_value.lower())
    # return generate_scatter(frame=df_clean)


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == "__main__":
    app.run_server(debug=True)
