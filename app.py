from typing import Dict, Any
import pandas as pd
import numpy as np

import plotly.express as px
from math import floor
import json
import dash
from dash import Dash, dcc, html, Input, Output, State
from generate_graphs import *

# https://www.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page Neighb maps
# https://capitalplanning.nyc.gov/capitalproject/846P-5FRESHN#12.88/40.5704/-74.1954 POI locations
# TODO Select price range of hotels (histogram) limit map view to those hotels
# TODO Limit results to distance from park for example


df_clean = pd.read_csv("AirbnbClean.csv", low_memory=False, index_col=0)
df_means = pd.read_csv("neighb_means.csv")

neighb = json.load(open("neighb.json"))
df_clean = pd.read_csv("AirbnbClean.csv", index_col=0, low_memory=False)
df_neighbreviewmean = pd.read_csv("neighb_means.csv", low_memory=False)

df_clean["scaled"] = df_clean["review rate number"]
mean = floor(df_clean["scaled"].mean())
df_clean["scaled"].fillna(mean, inplace=True)
df_clean.dropna(subset=["number of reviews"], inplace=True)
df_clean["number of reviews"] = df_clean["number of reviews"] * 100

filter_val = "price"
min_val = min(df_clean["price"])
max_val = max(df_clean["price"])

df_subset = df_clean[df_clean[filter_val >= min_val & filter_val <= max_val]]
px.set_mapbox_access_token("pk.eyJ1IjoicG5pZXJvcCIsImEiOiJjbGFxdnJkNGMwMGtuM3FwYmN5czV5NnowIn0.mYk_lZjfdsJQhxbTBsRbmw")
# fig = px.scatter_mapbox(df_test, lat="lat", lon="long", color="scaled", size="number of reviews",
#                         color_continuous_scale="aggrnyl_r")
# fig.update_layout({
#     "margin": dict(l=20, r=20, t=20, b=20),
#     "showlegend": True,
#     "paper_bgcolor": "rgba(0,0,0,0)",
#     "plot_bgcolor": "rgba(0,0,0,0)",
#     "font": {"color": "white"},
#     "mapbox_style":"dark"})
# # fig.update_traces(cluster=dict(enabled=True, color=["blue","red","green"], maxzoom=11))
# # fig.show()
#
# fig2 = px.choropleth_mapbox(df_clean, geojson=neighb, locations="neighbourhood",
# featureidkey="properties.neighborhood", color="scaled", center={"lat": 40.7128, "lon": -74.0060}, zoom=10,
# color_continuous_scale="aggrnyl_r") fig2.update_geos(fitbounds="locations", visible=False) fig2.update_layout({
# "margin": dict(l=20, r=20, t=20, b=20), "paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)",
# "font": {"color": "white"}, "mapbox_style":"dark"})

# fig = generate_scattermap(frame=df_clean, color_var="distanceTimeSquare", size_var="review rate number")
fig2 = generate_choropleth(frame=df_neighbreviewmean, poly_data=neighb, color_var="review rate number")
fig_scat = generate_scatter(frame=df_clean, xval="distanceTimeSquare", yval="price")
app = dash.Dash(eager_loading=True)

app.layout = html.Div(className='page', children=[
    html.Div(children=[
        html.H1("Dashboard Prototype", style=dict(width='75%'), id="title_field"),
        dcc.RadioItems(
            [
                {
                    "label": html.Div(['Light'], style={'color': 'White', 'font-size': 20}),
                    "value": "Light",
                },
                {
                    "label": html.Div(['Dark'], style={'color': 'White', 'font-size': 20}),
                    "value": "Dark",
                },
            ], value='Dark', inline=True
            , id="testid")], style=dict(display='flex')),
    html.Div(children=[
        dcc.Dropdown(df_clean.columns, id="drop1", value="number of reviews",
                     style=dict(width='50%')),
        dcc.Dropdown(df_clean.columns, id="drop2", value="review rate number",
                     style=dict(width='50%'))],
        style=dict(display='flex')
    ),
    html.Div(children=[
        dcc.Graph(id="scatter_map", style={'display': 'inline-block'}),
        dcc.Store(id="fig_store"),
        dcc.Graph(id="ch_graph", figure=fig2, style={'display': 'inline-block'}),

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H3("XVal", style=dict(color="White")),
                    dcc.Dropdown(df_clean.columns, value="number of reviews", id="drop_x", style=dict(width="50%")),
                    html.H3("YVal", style=dict(color="White")),
                    dcc.Dropdown(df_clean.columns, value="number of reviews", id="drop_y", style=dict(width="50%"))
                ], style=dict(display="flex")),
                dcc.Graph(id="scatter")]),
            dcc.Graph(id="histogram"),
            dcc.RangeSlider(min(df_clean["price"]),max(df_clean["price"]), 100, id="slider")]
)
    ])
])


@app.callback(
    Output("fig_store", "data"),
    Input("drop1", "value"),
    Input("drop2", "value")
)
def update_graphs(sizeval, colorvar):
    fig_new = generate_scattermap(frame=df_clean, color_var=colorvar, size_var=sizeval)
    return fig_new


# change the id in the state and output to change the id of your plot

# There's a bug with the dynamic updating of mapbox figures in Plotly right now this is the workaround using some JS
app.clientside_callback(
    '''
    function (figure, graph_id) {
        if(figure === undefined) {
            return {'data': [], 'layout': {}};
        }
        var graphDiv = document.getElementById(graph_id);
        var data = figure.data;
        var layout = figure.layout;        
        Plotly.newPlot(graphDiv, data, layout);
    }
    ''',
    Output('scatter_map', 'figure'),
    Input('fig_store', 'data'),
    State('scatter_map', 'id')
)


@app.callback(
    Output("scatter", "figure"),
    Input("drop_x", "value"),
    Input("drop_y", "value"))
def update_scatter(xval, yval):
    return generate_scatter(frame=df_clean, xval=xval, yval=yval)


@app.callback(
    Output("histogram", "figure"),
    Input("slider", "value"))
def update_hist(val):
    if val:
        fig = generate_hist(df_clean, "price", val[0], val[1])
    else:
        fig = generate_hist(df_clean, "price")
    return fig


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == "__main__":
    app.run_server(debug=True)
