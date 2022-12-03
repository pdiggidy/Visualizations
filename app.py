from typing import Dict, Any
import pandas as pd
import numpy as np

import plotly.express as px
from math import floor
import json
from dash import Dash, dcc, html, Input, Output, State
from generate_graphs import *
from time import monotonic

import dash


df_clean = pd.read_csv("AirbnbClean.csv", low_memory=False, index_col=0)
df_means = pd.read_csv("neighb_means.csv")
print(df_means.columns)

neighb = json.load(open("neighb.json"))

df_clean["scaled"] = df_clean["review rate number"]
mean = floor(df_clean["scaled"].mean())
df_clean["scaled"].fillna(mean, inplace=True)
df_clean.dropna(subset=["number of reviews"], inplace=True)
df_clean["number of reviews"] = df_clean["number of reviews"] * 100

df_test = df_clean
px.set_mapbox_access_token("pk.eyJ1IjoicG5pZXJvcCIsImEiOiJjbGFxdnJkNGMwMGtuM3FwYmN5czV5NnowIn0.mYk_lZjfdsJQhxbTBsRbmw")

# fig2 = generate_choropleth(frame=df_neighbreviewmean, poly_data=neighb)
fig_scat = generate_scatter(frame=df_clean, xval="distanceTimeSquare", yval="price")
app = dash.Dash(eager_loading=True)

app.layout = html.Div(className='page', children=[
    html.H1("Dashboard Prototype"),
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
        ], value='Dark'
    ),
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
        dcc.Graph(id="ch_graph", style={'display': 'inline-block'}),
        dcc.Store(id="ch_graph_store"),

        html.Div(children=[
            html.Div(children=[
                html.H3("XVal", style=dict(color="White")),
                dcc.Dropdown(df_clean.columns, value="number of reviews", id="drop_x", style=dict(width="50%")),
                html.H3("YVal", style=dict(color="White")),
                dcc.Dropdown(df_clean.columns, value="number of reviews", id="drop_y", style=dict(width="50%"))
            ], style=dict(display="flex")),
            dcc.Graph(id="scatter")
        ])
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

# Theres a bug with the dynamic updating of mapbox figures in Plotly right now this is the workaround using some JS
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
    Output("ch_graph_store", "data"),
    Input("drop2", "value"),
)
def update_graphs(colorvar):
    fig_new = generate_choropleth(frame=df_means, poly_data=neighb, color_var=colorvar)
    return fig_new


# change the id in the state and output to change the id of your plot

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
    Output('ch_graph', 'figure'),
    Input('ch_graph_store', 'data'),
    State('ch_graph', 'id')
)


@app.callback(
    Output("scatter", "figure"),
    Input("drop_x", "value"),
    Input("drop_y", "value"))
def update_scatter(xval, yval):
    return generate_scatter(frame=df_clean, xval=xval, yval=yval)


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == "__main__":
    app.run_server(debug=True)